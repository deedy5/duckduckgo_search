import logging
import re
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from html import unescape
from time import sleep
from typing import Deque, Dict, Iterator, Optional
from urllib.parse import unquote

import requests
from requests.exceptions import HTTPError, JSONDecodeError, Timeout
from requests.models import Response

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Referer": "https://duckduckgo.com/",
}
REGEX_500_IN_URL = re.compile(r"[0-9]{3}-[0-9]{2}.js")
REGEX_STRIP_TAGS = re.compile("<.*?>")


@dataclass
class MapsResult:
    title: Optional[str] = None
    address: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    url: Optional[str] = None
    desc: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None
    source: Optional[str] = None
    links: Optional[str] = None
    hours: Optional[Dict] = None


class DDGS:
    """DuckDuckgo_search class to get search results from duckduckgo.com"""

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> None:
        self.headers = headers if headers else HEADERS
        self._session = requests.Session()
        self._session.headers.update(headers if headers else HEADERS)
        self._session.proxies.update(proxies if proxies else {})
        self._timeout = timeout

    def _get_url(self, method: str, url: str, **kwargs) -> Optional[Response]:
        for i in range(3):
            try:
                resp = self._session.request(
                    method, url, timeout=self._timeout, **kwargs
                )
                if self._is_500_in_url(resp.url):
                    raise requests.HTTPError
                resp.raise_for_status()
                return resp
            except (HTTPError, Timeout) as ex:
                logger.warning(f"_get_url() {url} {type(ex).__name__} {ex}")
                if i < 2:
                    sleep(2**i)
        return None

    def _get_vqd(self, keywords: str) -> Optional[str]:
        """Get vqd value for a search query."""
        resp = self._get_url("POST", "https://duckduckgo.com", data={"q": keywords})
        if resp:
            for c1, c2 in (
                (b'vqd="', b'"'),
                (b"vqd=", b"&"),
                (b"vqd='", b"'"),
            ):
                try:
                    start = resp.content.index(c1) + len(c1)
                    end = resp.content.index(c2, start)
                    return resp.content[start:end].decode()
                except ValueError:
                    logger.warning(f"_get_vqd() keywords={keywords} vqd not found")
        return None

    def _is_500_in_url(self, url: str) -> bool:
        """something like '506-00.js' inside the url"""
        return bool(REGEX_500_IN_URL.search(url))

    def _normalize(self, raw_html: str) -> str:
        """strip HTML tags"""
        if raw_html:
            return unescape(re.sub(REGEX_STRIP_TAGS, "", raw_html))
        return ""

    def text(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
    ) -> Iterator[dict]:
        """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.

        Yields:
            dict with search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        if not vqd:
            return None

        safesearch_base = {"on": 1, "moderate": -1, "off": -2}
        payload = {
            "q": keywords,
            "l": region,
            "p": safesearch_base[safesearch.lower()],
            "s": 0,
            "df": timelimit,
            "o": "json",
            "vqd": vqd,
        }

        cache = set()
        for _ in range(10):
            resp = self._get_url(
                "GET", "https://links.duckduckgo.com/d.js", params=payload
            )
            if resp is None:
                break
            try:
                page_data = resp.json().get("results", None)
            except (AttributeError, JSONDecodeError):
                break

            if page_data:
                result_exists = False
                for row in page_data:
                    if "n" in row:
                        payload["s"] = row["n"].split("s=")[-1].split("&")[0]  # next page
                    href = row.get("u", None)
                    if (
                        href
                        and href not in cache
                        and href != f"http://www.google.com/search?q={keywords}"
                    ):
                        cache.add(href)
                        body = self._normalize(row["a"])
                        if body:
                            result_exists = True
                            yield {
                                "title": self._normalize(row["t"]),
                                "href": href,
                                "body": body,
                            }
                    elif result_exists is False:
                        break
                if result_exists is False:
                    break

    def images(
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
    ) -> Iterator[dict]:
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

        Yields:
            dict with image search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        if not vqd:
            return None

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
            "s": 0,
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{size},{color},{type_image},{layout},{license_image}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        for _ in range(10):
            resp = self._get_url("GET", "https://duckduckgo.com/i.js", params=payload)
            if resp is None:
                break
            try:
                resp_json = resp.json()
            except (AttributeError, JSONDecodeError):
                break

            page_data = resp_json.get("results", None)
            if page_data:
                result_exists = False
                for row in page_data:
                    image_url = row.get("image", None)
                    if image_url and image_url not in cache:
                        cache.add(image_url)
                        result_exists = True
                        yield {
                            "title": row["title"],
                            "image": image_url,
                            "thumbnail": row["thumbnail"],
                            "url": row["url"],
                            "height": row["height"],
                            "width": row["width"],
                            "source": row["source"],
                        }
                next = resp_json.get("next", None)
                if next:
                    payload["s"] = next.split("s=")[-1].split("&")[0]
                if next is None or result_exists is False:
                    break

    def videos(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        resolution: Optional[str] = None,
        duration: Optional[str] = None,
        license_videos: Optional[str] = None,
    ) -> Iterator[dict]:
        """DuckDuckGo videos search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            resolution: high, standart. Defaults to None.
            duration: short, medium, long. Defaults to None.
            license_videos: creativeCommon, youtube. Defaults to None.

        Yields:
            dict with videos search results

        """
        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        if not vqd:
            return None

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
            resp = self._get_url("GET", "https://duckduckgo.com/v.js", params=payload)
            if resp is None:
                break
            try:
                resp_json = resp.json()
            except (AttributeError, JSONDecodeError):
                break

            page_data = resp_json.get("results", None)
            if page_data:
                result_exists = False
                for row in page_data:
                    if row["content"] not in cache:
                        cache.add(row["content"])
                        result_exists = True
                        yield row
                next = resp_json.get("next", None)
                if next:
                    payload["s"] = next.split("s=")[-1].split("&")[0]
                if not result_exists or not next:
                    break

    def news(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
    ) -> Iterator[dict]:
        """DuckDuckGo news search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.

        Yields:
            dict with news search results.

        """
        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        if not vqd:
            return None

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
            resp = self._get_url(
                "GET", "https://duckduckgo.com/news.js", params=payload
            )
            if resp is None:
                break
            try:
                resp_json = resp.json()
            except (AttributeError, JSONDecodeError):
                break

            page_data = resp_json.get("results", None)
            if page_data:
                result_exists = False
                for row in page_data:
                    if row["url"] not in cache:
                        cache.add(row["url"])
                        result_exists = True
                        yield {
                            "date": datetime.utcfromtimestamp(row["date"]).isoformat(),
                            "title": row["title"],
                            "body": self._normalize(row["excerpt"]),
                            "url": row["url"],
                            "image": row.get("image", None),
                            "source": row["source"],
                        }
                next = resp_json.get("next", None)
                if next:
                    payload["s"] = next.split("s=")[-1].split("&")[0]
                if not result_exists or not next:
                    break

    def answers(
        self,
        keywords: str,
    ) -> Iterator[dict]:
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

        resp = self._get_url("GET", "https://api.duckduckgo.com/", params=payload)
        if resp is None:
            return None
        try:
            page_data = resp.json()
        except (AttributeError, JSONDecodeError):
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
        resp = self._get_url("GET", "https://api.duckduckgo.com/", params=payload)
        if resp is None:
            return None
        try:
            page_data = resp.json().get("RelatedTopics", None)
        except (AttributeError, JSONDecodeError):
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

    def suggestions(
        self,
        keywords: str,
        region: str = "wt-wt",
    ) -> Iterator[dict]:
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
        resp = self._get_url("GET", "https://duckduckgo.com/ac", params=payload)
        if resp is None:
            return None
        try:
            page_data = resp.json()
            for r in page_data:
                yield r
        except (AttributeError, JSONDecodeError):
            pass

    def maps(
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
    ) -> Iterator[dict]:
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

        Yields:
            dict with maps search results
        """

        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        if not vqd:
            return None

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
                resp = self._get_url(
                    "GET",
                    "https://nominatim.openstreetmap.org/search.php",
                    params=params,
                )
                if resp is None:
                    return None

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
        logging.debug(f"bbox coordinates\n{lat_t} {lon_l}\n{lat_b} {lon_r}")

        # сreate a queue of search squares (bboxes)
        work_bboxes: Deque = deque()
        work_bboxes.append((lat_t, lon_l, lat_b, lon_r))

        # bbox iterate
        cache = set()
        stop_find = False
        while work_bboxes and not stop_find:
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
            resp = self._get_url(
                "GET", "https://duckduckgo.com/local.js", params=params
            )
            if resp is None:
                break
            try:
                page_data = resp.json().get("results", [])
            except (AttributeError, JSONDecodeError):
                break
            
            if page_data:
                for res in page_data:
                    result = MapsResult()
                    result.title = res["name"]
                    result.address = res["address"]
                    if f"{result.title} {result.address}" in cache:
                        continue
                    else:
                        cache.add(f"{result.title} {result.address}")
                        result.country_code = res["country_code"]
                        result.url = res["website"]
                        result.phone = res["phone"]
                        result.latitude = res["coordinates"]["latitude"]
                        result.longitude = res["coordinates"]["longitude"]
                        result.source = unquote(res["url"])
                        if res["embed"]:
                            result.image = res["embed"].get("image", "")
                            result.links = res["embed"].get("third_party_links", "")
                            result.desc = res["embed"].get("description", "")
                        result.hours = res["hours"]
                        yield result.__dict__

                # divide the square into 4 parts and add to the queue
                if len(page_data) >= 15:
                    lat_middle = (lat_t + lat_b) / 2
                    lon_middle = (lon_l + lon_r) / 2
                    bbox1 = (lat_t, lon_l, lat_middle, lon_middle)
                    bbox2 = (lat_t, lon_middle, lat_middle, lon_r)
                    bbox3 = (lat_middle, lon_l, lat_b, lon_middle)
                    bbox4 = (lat_middle, lon_middle, lat_b, lon_r)
                    work_bboxes.extendleft([bbox1, bbox2, bbox3, bbox4])

    def translate(
        self,
        keywords: str,
        from_: Optional[str] = None,
        to: str = "en",
    ) -> Optional[dict]:
        """DuckDuckGo translate

        Args:
            keywords: string or a list of strings to translate
            from_: translate from (defaults automatically). Defaults to None.
            to: what language to translate. Defaults to "en".

        Returns:
            dict with translated keywords.
        """

        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd("translate")
        if not vqd:
            return None

        payload = {
            "vqd": vqd,
            "query": "translate",
            "from": from_,
            "to": to,
        }

        resp = self._get_url(
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
        except (AttributeError, JSONDecodeError):
            page_data = None
        return page_data