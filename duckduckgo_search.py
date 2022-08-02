import csv
import json
import os
import re
import unicodedata
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from time import sleep

import click
import requests
from lxml import html

__version__ = "1.8.1"


session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
}
session.headers.update(headers)


@dataclass
class MapsResult:
    """Dataclass for ddg_maps search results"""

    title: str = None
    address: str = None
    country_code: str = None
    latitude: str = None
    longitude: str = None
    url: str = None
    desc: str = None
    phone: str = None
    image: str = None
    source: str = None
    links: dict = None
    hours: dict = None


def _save_json(jsonfile, data):
    with open(jsonfile, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _save_csv(csvfile, data):
    headers = data[0].keys()
    with open(csvfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def _save_image(image_url, dir_path, filename):
    resp = requests.get(image_url, headers=headers, timeout=30)
    if resp.status_code == 200:
        with open(os.path.join(dir_path, _slugify(filename)), "wb") as f:
            f.write(resp.content)


def _slugify(filename):
    """
    Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """

    filename = unicodedata.normalize("NFC", filename)
    filename = re.sub(r"[^\w\s-]", "", filename.lower())
    return re.sub(r"[-\s]+", "-", filename).strip("-_")


def _normalize(text):
    if text:
        body = html.fromstring(text)
        return html.tostring(body, method="text", encoding="unicode")


def ddg(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=28,
    output=None,
):
    """DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year);
    max_results = 28 gives a number of results not less than 28,
                  maximum DDG gives out about 200 results,
    output: csv, json, print.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": keywords,
    }
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )
    sleep(0.75)

    # search
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}
    params = {
        "q": keywords,
        "l": region,
        "p": safesearch_base[safesearch],
        "s": 0,
        "df": time,
        "o": "json",
        "vqd": vqd,
    }
    results, cache = [], set()
    while len(results) < max_results and params["s"] < 200:
        resp = session.get("https://links.duckduckgo.com/d.js", params=params)
        data = resp.json().get("results", None)
        if not data:
            break

        for r in data:
            try:
                s = r["n"].split("s=")[1].split("&")[0]
                params["s"] = int(s) - int(s) % 2
                break
            except:
                if r["u"] not in cache:
                    cache.add(r["u"])
                    title = _normalize(r["t"])
                    href = r["u"]
                    body = _normalize(r["a"])
                    if body:
                        results.append(
                            {
                                "title": title,
                                "href": href,
                                "body": body,
                            }
                        )
        sleep(0.75)

    """ using html method
    payload = {
        'q': keywords,
        'l': region,
        'p': safesearch_base[safesearch],
        'df': time
        }
    results = []
    while True:
        res = session.post('https://html.duckduckgo.com/html', data=payload, **kwargs)
        tree = html.fromstring(res.text)
        if tree.xpath('//div[@class="no-results"]/text()'):
            return results
        for element in tree.xpath('//div[contains(@class, "results_links")]'):
            results.append({'title': element.xpath('.//a[contains(@class, "result__a")]/text()')[0],
                            'href': element.xpath('.//a[contains(@class, "result__a")]/@href')[0],
                            'body': ''.join(element.xpath('.//a[contains(@class, "result__snippet")]//text()')),})
        if len(results) >= max_results:
            return results
        next_page = tree.xpath('.//div[@class="nav-link"]')[-1]
        names = next_page.xpath('.//input[@type="hidden"]/@name')
        values = next_page.xpath('.//input[@type="hidden"]/@value')
        payload = {n: v for n, v in zip(names, values)}
        sleep(2)
    """
    results = results[:max_results]

    #output
    keywords = keywords.replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()
    return results


def ddg_images(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    size=None,
    color=None,
    type_image=None,
    layout=None,
    license_image=None,
    max_results=100,
    output=None,
    download=False,
):
    """DuckDuckGo images search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: Day, Week, Month, Year;
    size: Small, Medium, Large, Wallpaper;
    color: color, Monochrome, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Black, Gray, Teal, White;
    type_image: photo, clipart, gif, transparent, line;
    layout: Square, Tall, Wide;
    license_image: any (All Creative Commons), Public (Public Domain), Share (Free to Share and Use),
             ShareCommercially (Free to Share and Use Commercially), Modify (Free to Modify, Share, and Use),
             ModifyCommercially (Free to Modify, Share, and Use Commercially);
    max_results: number of results, maximum ddg_images gives out 1000 results;
    output: csv, json, print;
    download: if True, download and save images to 'keywords' folder.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": keywords,
    }
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )

    # get images
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}

    time = f"time:{time}" if time else ""
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
        "f": f"{time},{size},{color},{type_image},{layout},{license_image}",
        "p": safesearch_base[safesearch],
    }

    results = []
    while payload["s"] < max_results or len(results) < max_results:
        resp = session.get("https://duckduckgo.com/i.js", params=payload)
        data = resp.json().get("results", None)
        if not data:
            break
        for d in data:
            r = {
                "title": d["title"],
                "image": d["image"],
                "thumbnail": d["thumbnail"],
                "url": d["url"],
                "height": d["height"],
                "width": d["width"],
                "source": d["source"],

            }
            results.append(r)
        payload["s"] += 100
    results = results[:max_results]

    #output
    keywords = keywords.replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_images_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_images_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()

    #download
    if download:
        print("Downloading images. Wait...")
        lenresults = len(results)
        keywords = keywords.replace('"', "'")
        path = f"{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(path, exist_ok=True)
        futures = []
        with ThreadPoolExecutor(30) as executor:
            for r in results:
                future = executor.submit(_save_image, r["image"], path, r["title"])
                futures.append(future)
            for i, future in enumerate(as_completed(futures), start=1):
                print(f"{i}/{lenresults}")

        print("Done.")
    return results


def ddg_videos(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    resolution=None,
    duration=None,
    license_videos=None,
    max_results=62,
    output=None,
):
    """DuckDuckGo videos search
    keywords: keywords for query;
    safesearch: On (p = 1), Moderate (p = -1), Off (p = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: d, w, m (published after);
    resolution: high, standart;
    duration: short, medium, long;
    license_videos: creativeCommon, youtube;
    max_results: number of results, maximum ddg_videos gives out 1000 results;
    output: csv, json, print.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": keywords,
    }
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )

    # get videos
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}

    time = f"publishedAfter:{time}" if time else ""
    resolution = f"videoDefinition:{resolution}" if resolution else ""
    duration = f"videoDuration:{duration}" if duration else ""
    license_videos = f"videoLicense:{license_videos}" if license_videos else ""
    payload = {
        "l": region,
        "o": "json",
        "s": 0,
        "q": keywords,
        "vqd": vqd,
        "f": f"{time},{resolution},{duration},{license_videos}",
        "p": safesearch_base[safesearch],
    }

    results, cache = [], set()
    while payload["s"] < max_results or len(results) < max_results:
        res = session.get("https://duckduckgo.com/v.js", params=payload)
        data = res.json()
        page_data = data.get("results", None)
        page_results = []
        if not page_data:
            break
        for e in page_data:
            if e["content"] not in cache:
                page_results.append(e)
                cache.add(e["content"])
        if not page_results:
            break
        results.extend(page_results)
        payload["s"] += 62
    results = results[:max_results]

    #output
    keywords = keywords.replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_videos_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_videos_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()

    return results


def ddg_news(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=30,
    output=None,
):
    """DuckDuckGo news search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month);
    max_results = 30, maximum DDG_news gives out 240 results;
    output: csv, json, print.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": keywords,
    }
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )

    # get news
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}
    params = {
        "l": region,
        "o": "json",
        "noamp": "1",
        "q": keywords,
        "vqd": vqd,
        "p": safesearch_base[safesearch],
        "df": time,
        "s": 0,
    }
    data_previous, cache = [], set()
    results = []
    while params["s"] < min(max_results, 240) or len(results) < max_results:
        resp = session.get("https://duckduckgo.com/news.js", params=params)
        data = resp.json().get("results", None)
        if not data:
            break
        if data_previous and data == data_previous:
            break
        else:
            data_previous = data
        for r in data:
            title = r["title"]
            if title in cache:
                continue
            else:
                cache.add(title)
            results.append(
                {
                    "date": datetime.utcfromtimestamp(r["date"]).isoformat(),
                    "title": title,
                    "body": _normalize(r["excerpt"]),
                    "url": r["url"],
                    "image": r.get("image", ""),
                    "source": r["source"],
                }
            )
        params["s"] += 30
        sleep(0.2)
    results = results[:max_results]
    results = sorted(results, key=lambda x: x["date"], reverse=True)
    #output
    keywords = keywords.replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_news_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_news_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()
    return results


def ddg_maps(
    keywords,
    place=None,
    street=None,
    city=None,
    county=None,
    state=None,
    country=None,
    postalcode=None,
    latitude=None,
    longitude=None,
    radius=0,
    max_results=None,
    output=None,
):
    """DuckDuckGo maps search
    keywords: keywords for query;
    place: simplified search - if set, the other parameters are not used;
    street: house number/street;
    city: city of search;
    county: county of search;
    state: state of search;
    country: country of search;
    postalcode: postalcode of search;
    latitude: geographic coordinate that specifies the north–south position;
    longitude: geographic coordinate that specifies the east–west position;
        if latitude and longitude are set, the other parameters are not used.
    radius: expand the search square by the distance in kilometers,
    max_results: maximum number of results;
    output: csv, json, print.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": keywords,
    }
    resp = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(resp.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )

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
            params = {
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
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search.php",
            params=params,
            headers=headers,
        )

        coordinates = resp.json()[0]["boundingbox"]
        lat_t, lon_l = Decimal(coordinates[1]), Decimal(coordinates[2])
        lat_b, lon_r = Decimal(coordinates[0]), Decimal(coordinates[3])

    # if a radius is specified, expand the search square
    lat_t += Decimal(radius) * Decimal(0.008983)
    lat_b -= Decimal(radius) * Decimal(0.008983)
    lon_l -= Decimal(radius) * Decimal(0.008983)
    lon_r += Decimal(radius) * Decimal(0.008983)
    print(f"bbox coordinates\n{lat_t} {lon_l}\n{lat_b} {lon_r}")

    # сreate a queue of search squares (bboxes)
    work_bboxes = deque()
    work_bboxes.append((lat_t, lon_l, lat_b, lon_r))

    # bbox iterate
    results, cache = [], set()
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
        resp = session.get("https://duckduckgo.com/local.js", params=params)
        try:
            data = resp.json()["results"]
        except:
            stop_find = True
            break

        for res in data:
            r = MapsResult()
            r.title = res["name"]
            r.address = res["address"]
            if r.title + r.address in cache:
                continue
            else:
                cache.add(r.title + r.address)
                r.country_code = res["country_code"]
                r.url = res["website"]
                r.phone = res["phone"]
                r.latitude = res["coordinates"]["latitude"]
                r.longitude = res["coordinates"]["longitude"]
                r.source = _normalize(res["url"])
                if res["embed"]:
                    r.image = res["embed"].get("image", "")
                    r.links = res["embed"].get("third_party_links", "")
                    r.desc = res["embed"].get("description", "")
                r.hours = res["hours"]
                results.append(r.__dict__)
                if max_results and len(results) >= max_results:
                    stop_find = True
                    break

        # divide the square into 4 parts and add to the queue
        if len(data) >= 15:
            lat_middle = (lat_t + lat_b) / 2
            lon_middle = (lon_l + lon_r) / 2
            bbox1 = (lat_t, lon_l, lat_middle, lon_middle)
            bbox2 = (lat_t, lon_middle, lat_middle, lon_r)
            bbox3 = (lat_middle, lon_l, lat_b, lon_middle)
            bbox4 = (lat_middle, lon_middle, lat_b, lon_r)
            work_bboxes.extendleft([bbox1, bbox2, bbox3, bbox4])

        print(f"Found {len(results)}")

    #output
    keywords = keywords.replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_maps_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_maps_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()
    return results


def ddg_translate(keywords, from_=None, to="en", output=None):
    """DuckDuckGo translate
    keywords: string or a list of strings to translate;
    from_: what language to translate from (defaults automatically),
    to: what language to translate (defaults to en),
    output: print, csv, json.
    """

    if not keywords:
        return None

    # get vqd
    payload = {
        "q": "translate",
    }
    resp = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(resp.text)
    vqd = (
        tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
        .split("vqd='")[-1]
        .split("';")[0]
    )

    # translate
    params = {
        "vqd": vqd,
        "query": "translate",
        "from": from_,
        "to": to,
    }

    if isinstance(keywords, str):
        keywords = [keywords]

    results = []
    for data in keywords:
        resp = session.post(
            "https://duckduckgo.com/translation.js",
            params=params,
            data=data.encode("utf-8"),
        )
        result = resp.json()
        result["original"] = data
        results.append(result)

    #output
    keywords = keywords[0].replace('"', "'")
    if output == 'csv':
        _save_csv(
            f"ddg_translate_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", results
        )
    elif output == 'json':
        _save_json(
            f"ddg_translate_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", results
        )
    elif output == 'print':
        for i, x in enumerate(results, start=1):
            print(f"{i}.", json.dumps(x, ensure_ascii=False, indent=2))
            input()
    return results


@click.group(chain=True)
def cli():
    pass


@cli.command()
@click.option("-k", "--keywords", help="text search, keywords for query")
@click.option("-r", "--region", default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m, y")
@click.option("-m", "--max_results", default=28,
    help="number of results (not less than 28), maximum DDG gives out about 200 results",)
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
def text(*args, **kwargs):
    return ddg(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option("-r", "--region", default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="Day, Week, Month, Year")
@click.option("-size", "--size", default=None, help="Small, Medium, Large, Wallpaper")
@click.option("-c", "--color", default=None,
    help="color, Monochrome, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Black, Gray, Teal, White",)
@click.option("-type", "--type_image", default=None, help="photo, clipart, gif, transparent, line")
@click.option("-l", "--layout", default=None, help="Square, Tall, Wide")
@click.option("-lic", "--license_image", default=None,
    help="""any (All Creative Commons), Public (Public Domain), Share (Free to Share and Use),
        ShareCommercially (Free to Share and Use Commercially), Modify (Free to Modify, Share, and Use),
        ModifyCommercially (Free to Modify, Share, and Use Commercially)""",)
@click.option("-m", "--max_results", default=100, help="number of results (default=100)")
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
@click.option("-d", "--download", is_flag=True, default=False,
    help="download and save images to 'keywords' folder, default=False",)
def images(*args, **kwargs):
    return ddg_images(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option("-r", "--region", default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m (published after)")
@click.option("-res", "--resolution", default=None, help="high, standart")
@click.option("-d", "--duration", default=None, help="short, medium, long",)
@click.option("-lic", "--license_videos", default=None, help="creativeCommon, youtube",)
@click.option("-m", "--max_results", default=100, help="number of results (default=62)")
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
def videos(*args, **kwargs):
    return ddg_videos(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option("-r", "--region", default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m, y")
@click.option("-m", "--max_results", default=30,
    help="number of results (default=30)")
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
def news(*args, **kwargs):
    return ddg_news(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option("-p", "--place", default=None,
    help="simplified search - if set, the other parameters are not used",)
@click.option("-s", "--street", default=None, help="house number/street")
@click.option("-c", "--city", default=None, help="city of search")
@click.option("-county", "--county", default=None, help="county of search")
@click.option("-state", "--state", default=None, help="state of search")
@click.option("-country", "--country", default=None, help="country of search")
@click.option("-post", "--postalcode", default=None, help="postalcode of search")
@click.option("-lat", "--latitude", default=None,
    help="""geographic coordinate that specifies the north–south position,
            if latitude and longitude are set, the other parameters are not used""",)
@click.option("-lon", "--longitude", default=None,
    help="""geographic coordinate that specifies the east–west position,
            if latitude and longitude are set, the other parameters are not used""",)
@click.option("-r", "--radius", default=0,
    help="expand the search square by the distance in kilometers",)
@click.option("-m", "--max_results", help="number of results (default=None)")
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
def maps(*args, **kwargs):
    return ddg_maps(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="text for translation")
@click.option("-f", "--from_", help="de, ru, fr, etc. What language to translate from (defaults automatically)")
@click.option("-t", "--to", default="en", help="de, ru, fr, etc. What language to translate (defaults='en')")
@click.option("-o", "--output", default='print', help="print, csv, json, default=print")
def translate(*args, **kwargs):
    return ddg_translate(*args, **kwargs)


if __name__ == "__main__":
    cli(prog_name="duckduckgo_search")
