import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from time import sleep

from requests import ConnectionError

from .utils import _download_image, _save_csv, _save_json, get_vqd, session

logger = logging.getLogger(__name__)


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
    """DuckDuckGo images search.

    Args:
        keywords (str): keywords for query.
        region (str, optional): country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.
            Defaults to "wt-wt".
        safesearch (str, optional): On (kp = 1), Moderate (kp = -1), Off (kp = -2).
            Defaults to "Moderate".
        time (Optional[str], optional): Day, Week, Month, Year. Defaults to None.
        size (Optional[str], optional): Small, Medium, Large, Wallpaper. Defaults to None.
        color (Optional[str], optional): color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
        type_image (Optional[str], optional): photo, clipart, gif, transparent, line.
            Defaults to None.
        layout (Optional[str], optional): Square, Tall, Wide. Defaults to None.
        license_image (Optional[str], optional): any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
        max_results (Optional[int], optional): number of results, max 1000 results. Defaults to 100.
        output (Optional[str], optional): csv, json, print. Defaults to None.
        download (bool, optional): if True, download and save images to 'keywords' folder.
            Defaults to False.

    Returns:
        List[dict]: DuckDuckGo text search results.
    """

    if not keywords:
        return None

    vqd = get_vqd(keywords)
    if not vqd:
        return
    sleep(0.75)

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

    results, cache = [], set()
    while payload["s"] < max_results or len(results) < max_results:
        page_data = None
        try:
            resp = session.get("https://duckduckgo.com/i.js", params=payload)
            logger.info(f"{resp.status_code} {resp.url}")
            page_data = resp.json().get("results", None)
        except ConnectionError:
            logger.error("Connection Error.")
            break
        except Exception:
            logger.exception("Exception.", exc_info=True)
            break

        if not page_data:
            break

        page_results = []
        for row in page_data:
            if row["image"] not in cache:
                cache.add(row["image"])
                result = {
                    "title": row["title"],
                    "image": row["image"],
                    "thumbnail": row["thumbnail"],
                    "url": row["url"],
                    "height": row["height"],
                    "width": row["width"],
                    "source": row["source"],
                }
                page_results.append(result)
        if not page_results:
            break
        results.extend(page_results)
        # pagination
        payload["s"] += 100
        sleep(0.2)

    results = results[:max_results]

    # output
    keywords = keywords.replace('"', "'")
    if output == "csv":
        _save_csv(f"ddg_images_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.csv", results)
    elif output == "json":
        _save_json(
            f"ddg_images_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.json", results
        )
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=2))
            input()

    # download
    if download:
        print("Downloading images. Wait...")
        keywords = keywords.replace('"', "'")
        path = f"ddg_images_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
        os.makedirs(path, exist_ok=True)
        futures = []
        with ThreadPoolExecutor(30) as executor:
            for i, res in enumerate(results, start=1):
                filename = res["image"].split("/")[-1].split("?")[0]
                future = executor.submit(
                    _download_image, res["image"], path, f"{i}_{filename}"
                )
                futures.append(future)
            for i, future in enumerate(as_completed(futures), start=1):
                logger.info(f"{i}/{len(results)}")
                print(f"{i}/{len(results)}")

        print("Done.")
    return results
