import asyncio
import logging
import sys
from collections import deque
from datetime import datetime, timezone
from decimal import Decimal
from itertools import cycle
from typing import AsyncIterator, Deque, Dict, Optional, Set, Tuple

from lxml import html
from curl_cffi import requests

from .exceptions import DuckDuckGoSearchException
from .models import MapsResult
from .utils import _extract_vqd, _is_500_in_url, _normalize, _normalize_url, _random_browser, _text_extract_json

logger = logging.getLogger("duckduckgo_search.AsyncDDGS")
# Not working on Windows, NotImplementedError (https://curl-cffi.readthedocs.io/en/latest/faq/)
if sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class AsyncDDGS:
    """DuckDuckgo_search async class to get search results from duckduckgo.com

    Args:
        headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
        proxies (Union[dict, str], optional): Proxies for the HTTP client (can be dict or str). Defaults to None.
        timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
    """

    def __init__(self, headers=None, proxies=None, timeout=10) -> None:
        self.proxies = proxies if proxies and isinstance(proxies, dict) else {"http": proxies, "https": proxies}
        self._session = requests.AsyncSession(
            headers=headers, proxies=self.proxies, timeout=timeout, impersonate=_random_browser()
        )
        self._session.headers["Referer"] = "https://duckduckgo.com/"

    async def __aenter__(self) -> "AsyncDDGS":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._session.close()

    async def _get_url(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        try:
            resp = await self._session.request(method, url, **kwargs)
            logger.debug(f"_get_url() {url} {resp.status_code} {resp.http_version} {resp.elapsed} {len(resp.content)}")
            resp.raise_for_status()
            if _is_500_in_url(str(resp.url)) or resp.status_code == 202:
                raise DuckDuckGoSearchException("Ratelimit")
            if resp.status_code == 200:
                return resp
        except Exception as ex:
            raise DuckDuckGoSearchException(f"_get_url() {url} {type(ex).__name__}: {ex}")

    async def _get_vqd(self, keywords: str) -> Optional[str]:
        """Get vqd value for a search query."""
        resp = await self._get_url("POST", "https://duckduckgo.com", data={"q": keywords})
        if resp:
            return _extract_vqd(resp.content, keywords)

    async def text(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        backend: str = "api",
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            backend: api, html, lite. Defaults to api.
                api - collect data from https://duckduckgo.com,
                html - collect data from https://html.duckduckgo.com,
                lite - collect data from https://lite.duckduckgo.com.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.
        Yields:
            dict with search results.

        """
        if backend == "api":
            results = self._text_api(keywords, region, safesearch, timelimit, max_results)
        elif backend == "html":
            results = self._text_html(keywords, region, safesearch, timelimit, max_results)
        elif backend == "lite":
            results = self._text_lite(keywords, region, timelimit, max_results)

        results_counter = 0
        async for result in results:
            yield result
            results_counter += 1
            if max_results and results_counter >= max_results:
                break

    async def _text_api(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd(keywords)

        payload = {
            "q": keywords,
            "kl": region,
            "l": region,
            "bing_market": region,
            "s": "0",
            "df": timelimit,
            "vqd": vqd,
            # "o": "json",
            "sp": "0",
        }
        safesearch = safesearch.lower()
        if safesearch == "moderate":
            payload["ex"] = "-1"
        elif safesearch == "off":
            payload["ex"] = "-2"
        elif safesearch == "on":  # strict
            payload["p"] = "1"

        cache = set()
        for _ in range(11):
            resp = await self._get_url("GET", "https://links.duckduckgo.com/d.js", params=payload)
            if resp is None:
                return

            page_data = _text_extract_json(resp.content, keywords)
            if page_data is None:
                return

            result_exists, next_page_url = False, None
            for row in page_data:
                href = row.get("u", None)
                if href and href not in cache and href != f"http://www.google.com/search?q={keywords}":
                    cache.add(href)
                    body = _normalize(row["a"])
                    if body:
                        result_exists = True
                        yield {
                            "title": _normalize(row["t"]),
                            "href": _normalize_url(href),
                            "body": body,
                        }
                else:
                    next_page_url = row.get("n", None)
            if max_results is None or result_exists is False or next_page_url is None:
                return
            payload["s"] = next_page_url.split("s=")[1].split("&")[0]

    async def _text_html(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with search results.

        """
        assert keywords, "keywords is mandatory"

        self._session.headers["Referer"] = "https://html.duckduckgo.com/"
        safesearch_base = {"on": 1, "moderate": -1, "off": -2}
        payload = {
            "q": keywords,
            "s": "0",
            "kl": region,
            "p": safesearch_base[safesearch.lower()],
            "df": timelimit,
        }
        cache: Set[str] = set()
        for _ in range(11):
            resp = await self._get_url("POST", "https://html.duckduckgo.com/html", data=payload)
            if resp is None:
                return

            tree = html.fromstring(resp.content)
            if tree.xpath('//div[@class="no-results"]/text()'):
                return

            result_exists = False
            for e in tree.xpath('//div[contains(@class, "results_links")]'):
                href = e.xpath('.//a[contains(@class, "result__a")]/@href')
                href = href[0] if href else None
                if (
                    href
                    and href not in cache
                    and href != f"http://www.google.com/search?q={keywords}"
                    and not href.startswith("https://duckduckgo.com/y.js?ad_domain")
                ):
                    cache.add(href)
                    title = e.xpath('.//a[contains(@class, "result__a")]/text()')
                    body = e.xpath('.//a[contains(@class, "result__snippet")]//text()')
                    result_exists = True
                    yield {
                        "title": _normalize(title[0]) if title else None,
                        "href": _normalize_url(href),
                        "body": _normalize("".join(body)) if body else None,
                    }

            if max_results is None or result_exists is False:
                return
            next_page = tree.xpath('.//div[@class="nav-link"]')
            next_page = next_page[-1] if next_page else None
            if next_page is None:
                return

            names = next_page.xpath('.//input[@type="hidden"]/@name')
            values = next_page.xpath('.//input[@type="hidden"]/@value')
            payload = {n: v for n, v in zip(names, values)}

    async def _text_lite(
        self,
        keywords: str,
        region: str = "wt-wt",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            timelimit: d, w, m, y. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with search results.

        """
        assert keywords, "keywords is mandatory"

        self._session.headers["Referer"] = "https://lite.duckduckgo.com/"
        payload = {
            "q": keywords,
            "s": "0",
            "o": "json",
            "api": "d.js",
            "kl": region,
            "df": timelimit,
        }
        cache: Set[str] = set()
        for _ in range(11):
            resp = await self._get_url("POST", "https://lite.duckduckgo.com/lite/", data=payload)
            if resp is None:
                return

            if b"No more results." in resp.content:
                return

            tree = html.fromstring(resp.content)

            result_exists = False
            data = zip(cycle(range(1, 5)), tree.xpath("//table[last()]//tr"))
            for i, e in data:
                if i == 1:
                    href = e.xpath(".//a//@href")
                    href = href[0] if href else None
                    if (
                        href is None
                        or href in cache
                        or href == f"http://www.google.com/search?q={keywords}"
                        or href.startswith("https://duckduckgo.com/y.js?ad_domain")
                    ):
                        [next(data, None) for _ in range(3)]  # skip block(i=1,2,3,4)
                    else:
                        cache.add(href)
                        title = e.xpath(".//a//text()")[0]
                elif i == 2:
                    body = e.xpath(".//td[@class='result-snippet']//text()")
                    body = "".join(body).strip()
                elif i == 3:
                    result_exists = True
                    yield {
                        "title": _normalize(title),
                        "href": _normalize_url(href),
                        "body": _normalize(body),
                    }
            if max_results is None or result_exists is False:
                return
            next_page_s = tree.xpath("//form[./input[contains(@value, 'ext')]]/input[@name='s']/@value")
            if not next_page_s:
                return
            payload["s"] = next_page_s[0]
            payload["vqd"] = _extract_vqd(resp.content, keywords)

    async def images(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo images search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: Day, Week, Month, Year. Defaults to None.
            size: Small, Medium, Large, Wallpaper. Defaults to None.
            color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
                Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
            type_image: photo, clipart, gif, transparent, line.
                Defaults to None.
            layout: Square, Tall, Wide. Defaults to None.
            license_image: any (All Creative Commons), Public (PublicDomain),
                Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
                Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
                Use Commercially). Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with image search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": 1, "moderate": 1, "off": -1}
        timelimit = f"time:{timelimit}" if timelimit else ""
        size = f"size:{size}" if size else ""
        color = f"color:{color}" if color else ""
        type_image = f"type:{type_image}" if type_image else ""
        layout = f"layout:{layout}" if layout else ""
        license_image = f"license:{license_image}" if license_image else ""
        payload = {
            "l": region,
            "o": "json",
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{size},{color},{type_image},{layout},{license_image}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        for _ in range(10):
            resp = await self._get_url("GET", "https://duckduckgo.com/i.js", params=payload)
            if resp is None:
                return
            try:
                resp_json = resp.json()
            except Exception:
                return
            page_data = resp_json.get("results", None)
            if page_data is None:
                return

            result_exists = False
            for row in page_data:
                image_url = row.get("image", None)
                if image_url and image_url not in cache:
                    cache.add(image_url)
                    result_exists = True
                    yield {
                        "title": row["title"],
                        "image": _normalize_url(image_url),
                        "thumbnail": _normalize_url(row["thumbnail"]),
                        "url": _normalize_url(row["url"]),
                        "height": row["height"],
                        "width": row["width"],
                        "source": row["source"],
                    }
                    if max_results and len(cache) >= max_results:
                        return
            if max_results is None or result_exists is False:
                return
            next = resp_json.get("next", None)
            if next is None:
                return
            payload["s"] = next.split("s=")[-1].split("&")[0]

    async def videos(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        resolution: Optional[str] = None,
        duration: Optional[str] = None,
        license_videos: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo videos search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            resolution: high, standart. Defaults to None.
            duration: short, medium, long. Defaults to None.
            license_videos: creativeCommon, youtube. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with videos search results

        """
        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": 1, "moderate": -1, "off": -2}
        timelimit = f"publishedAfter:{timelimit}" if timelimit else ""
        resolution = f"videoDefinition:{resolution}" if resolution else ""
        duration = f"videoDuration:{duration}" if duration else ""
        license_videos = f"videoLicense:{license_videos}" if license_videos else ""
        payload = {
            "l": region,
            "o": "json",
            "s": 0,
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{resolution},{duration},{license_videos}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        for _ in range(10):
            resp = await self._get_url("GET", "https://duckduckgo.com/v.js", params=payload)
            if resp is None:
                return
            try:
                resp_json = resp.json()
            except Exception:
                return
            page_data = resp_json.get("results", None)
            if page_data is None:
                return

            result_exists = False
            for row in page_data:
                if row["content"] not in cache:
                    cache.add(row["content"])
                    result_exists = True
                    yield row
                    if max_results and len(cache) >= max_results:
                        return
            if max_results is None or result_exists is False:
                return
            next = resp_json.get("next", None)
            if next is None:
                return
            payload["s"] = next.split("s=")[-1].split("&")[0]

    async def news(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo news search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with news search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd(keywords)

        safesearch_base = {"on": 1, "moderate": -1, "off": -2}
        payload = {
            "l": region,
            "o": "json",
            "noamp": "1",
            "q": keywords,
            "vqd": vqd,
            "p": safesearch_base[safesearch.lower()],
            "df": timelimit,
            "s": 0,
        }

        cache = set()
        for _ in range(10):
            resp = await self._get_url("GET", "https://duckduckgo.com/news.js", params=payload)
            if resp is None:
                return
            try:
                resp_json = resp.json()
            except Exception:
                return
            page_data = resp_json.get("results", None)
            if page_data is None:
                return

            result_exists = False
            for row in page_data:
                if row["url"] not in cache:
                    cache.add(row["url"])
                    image_url = row.get("image", None)
                    result_exists = True
                    yield {
                        "date": datetime.fromtimestamp(row["date"], timezone.utc).isoformat(),
                        "title": row["title"],
                        "body": _normalize(row["excerpt"]),
                        "url": _normalize_url(row["url"]),
                        "image": _normalize_url(image_url) if image_url else None,
                        "source": row["source"],
                    }
                    if max_results and len(cache) >= max_results:
                        return
            if max_results is None or result_exists is False:
                return
            next = resp_json.get("next", None)
            if next is None:
                return
            payload["s"] = next.split("s=")[-1].split("&")[0]

    async def answers(self, keywords: str) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo instant answers. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.

        Yields:
            dict with instant answers results.

        """
        assert keywords, "keywords is mandatory"

        payload = {
            "q": f"what is {keywords}",
            "format": "json",
        }

        resp = await self._get_url("GET", "https://api.duckduckgo.com/", params=payload)
        if resp is None:
            yield None
        try:
            page_data = resp.json()
        except Exception:
            page_data = None

        if page_data:
            answer = page_data.get("AbstractText", None)
            url = page_data.get("AbstractURL", None)
            if answer:
                yield {
                    "icon": None,
                    "text": answer,
                    "topic": None,
                    "url": url,
                }

        # related:
        payload = {
            "q": f"{keywords}",
            "format": "json",
        }
        resp = await self._get_url("GET", "https://api.duckduckgo.com/", params=payload)
        if resp is None:
            yield None
        try:
            page_data = resp.json().get("RelatedTopics", None)
        except Exception:
            page_data = None

        if page_data:
            for i, row in enumerate(page_data):
                topic = row.get("Name", None)
                if not topic:
                    icon = row["Icon"].get("URL", None)
                    yield {
                        "icon": f"https://duckduckgo.com{icon}" if icon else None,
                        "text": row["Text"],
                        "topic": None,
                        "url": row["FirstURL"],
                    }
                else:
                    for subrow in row["Topics"]:
                        icon = subrow["Icon"].get("URL", None)
                        yield {
                            "icon": f"https://duckduckgo.com{icon}" if icon else None,
                            "text": subrow["Text"],
                            "topic": topic,
                            "url": subrow["FirstURL"],
                        }

    async def suggestions(self, keywords: str, region: str = "wt-wt") -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo suggestions. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

        Yields:
            dict with suggestions results.
        """

        assert keywords, "keywords is mandatory"

        payload = {
            "q": keywords,
            "kl": region,
        }
        resp = await self._get_url("GET", "https://duckduckgo.com/ac", params=payload)
        if resp is None:
            yield None
        try:
            page_data = resp.json()
            for r in page_data:
                yield r
        except Exception:
            pass

    async def maps(
        self,
        keywords: str,
        place: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        county: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postalcode: Optional[str] = None,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
        radius: int = 0,
        max_results: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Optional[str]]]:
        """DuckDuckGo maps search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query
            place: if set, the other parameters are not used. Defaults to None.
            street: house number/street. Defaults to None.
            city: city of search. Defaults to None.
            county: county of search. Defaults to None.
            state: state of search. Defaults to None.
            country: country of search. Defaults to None.
            postalcode: postalcode of search. Defaults to None.
            latitude: geographic coordinate (north–south position). Defaults to None.
            longitude: geographic coordinate (east–west position); if latitude and
                longitude are set, the other parameters are not used. Defaults to None.
            radius: expand the search square by the distance in kilometers. Defaults to 0.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Yields:
            dict with maps search results
        """

        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd(keywords)

        # if longitude and latitude are specified, skip the request about bbox to the nominatim api
        if latitude and longitude:
            lat_t = Decimal(latitude.replace(",", "."))
            lat_b = Decimal(latitude.replace(",", "."))
            lon_l = Decimal(longitude.replace(",", "."))
            lon_r = Decimal(longitude.replace(",", "."))
            if radius == 0:
                radius = 1
        # otherwise request about bbox to nominatim api
        else:
            if place:
                params: Dict[str, Optional[str]] = {
                    "q": place,
                    "polygon_geojson": "0",
                    "format": "jsonv2",
                }
            else:
                params = {
                    "street": street,
                    "city": city,
                    "county": county,
                    "state": state,
                    "country": country,
                    "postalcode": postalcode,
                    "polygon_geojson": "0",
                    "format": "jsonv2",
                }
            try:
                resp = await self._get_url(
                    "GET",
                    "https://nominatim.openstreetmap.org/search.php",
                    params=params,
                )
                if resp is None:
                    yield None

                coordinates = resp.json()[0]["boundingbox"]
                lat_t, lon_l = Decimal(coordinates[1]), Decimal(coordinates[2])
                lat_b, lon_r = Decimal(coordinates[0]), Decimal(coordinates[3])
            except Exception as ex:
                logger.debug(f"ddg_maps() keywords={keywords} {type(ex).__name__} {ex}")
                return

        # if a radius is specified, expand the search square
        lat_t += Decimal(radius) * Decimal(0.008983)
        lat_b -= Decimal(radius) * Decimal(0.008983)
        lon_l -= Decimal(radius) * Decimal(0.008983)
        lon_r += Decimal(radius) * Decimal(0.008983)
        logger.debug(f"bbox coordinates\n{lat_t} {lon_l}\n{lat_b} {lon_r}")

        # сreate a queue of search squares (bboxes)
        work_bboxes: Deque[Tuple[Decimal, Decimal, Decimal, Decimal]] = deque()
        work_bboxes.append((lat_t, lon_l, lat_b, lon_r))

        # bbox iterate
        cache = set()
        while work_bboxes:
            lat_t, lon_l, lat_b, lon_r = work_bboxes.pop()
            params = {
                "q": keywords,
                "vqd": vqd,
                "tg": "maps_places",
                "rt": "D",
                "mkexp": "b",
                "wiki_info": "1",
                "is_requery": "1",
                "bbox_tl": f"{lat_t},{lon_l}",
                "bbox_br": f"{lat_b},{lon_r}",
                "strict_bbox": "1",
            }
            resp = await self._get_url("GET", "https://duckduckgo.com/local.js", params=params)
            if resp is None:
                return
            try:
                page_data = resp.json().get("results", [])
            except Exception:
                return
            if page_data is None:
                return

            for res in page_data:
                result = MapsResult()
                result.title = res["name"]
                result.address = res["address"]
                if f"{result.title} {result.address}" in cache:
                    continue
                else:
                    cache.add(f"{result.title} {result.address}")
                    result.country_code = res["country_code"]
                    result.url = _normalize_url(res["website"])
                    result.phone = res["phone"]
                    result.latitude = res["coordinates"]["latitude"]
                    result.longitude = res["coordinates"]["longitude"]
                    result.source = _normalize_url(res["url"])
                    if res["embed"]:
                        result.image = res["embed"].get("image", "")
                        result.links = res["embed"].get("third_party_links", "")
                        result.desc = res["embed"].get("description", "")
                    result.hours = res["hours"]
                    yield result.__dict__
                    if max_results and len(cache) >= max_results:
                        return
            if max_results is None:
                return
            # divide the square into 4 parts and add to the queue
            if len(page_data) >= 15:
                lat_middle = (lat_t + lat_b) / 2
                lon_middle = (lon_l + lon_r) / 2
                bbox1 = (lat_t, lon_l, lat_middle, lon_middle)
                bbox2 = (lat_t, lon_middle, lat_middle, lon_r)
                bbox3 = (lat_middle, lon_l, lat_b, lon_middle)
                bbox4 = (lat_middle, lon_middle, lat_b, lon_r)
                work_bboxes.extendleft([bbox1, bbox2, bbox3, bbox4])

    async def translate(
        self, keywords: str, from_: Optional[str] = None, to: str = "en"
    ) -> Optional[Dict[str, Optional[str]]]:
        """DuckDuckGo translate

        Args:
            keywords: string or a list of strings to translate
            from_: translate from (defaults automatically). Defaults to None.
            to: what language to translate. Defaults to "en".

        Returns:
            dict with translated keywords.
        """

        assert keywords, "keywords is mandatory"

        vqd = await self._get_vqd("translate")

        payload = {
            "vqd": vqd,
            "query": "translate",
            "to": to,
        }
        if from_:
            payload["from"] = from_

        resp = await self._get_url(
            "POST",
            "https://duckduckgo.com/translation.js",
            params=payload,
            data=keywords.encode(),
        )
        if resp is None:
            return None
        try:
            page_data = resp.json()
            page_data["original"] = keywords
        except Exception:
            page_data = None
        return page_data
