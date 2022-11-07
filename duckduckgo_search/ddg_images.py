import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .utils import SESSION, _do_output, _download_file, _get_vqd

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
    """DuckDuckGo images search. Query params: https://duckduckgo.com/params

    Args:
        keywords (str): keywords for query.
        region (str, optional): wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): On, Moderate, Off. Defaults to "Moderate".
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
        max_results (int, optional): maximum number of results, max=1000. Defaults to 100.
        output (Optional[str], optional): csv, json. Defaults to None.
        download (bool, optional): if True, download and save images to 'keywords' folder.
            Defaults to False.

    Returns:
        Optional[List[dict]]: DuckDuckGo text search results.
    """

    if not keywords:
        return None

    # get vqd
    vqd = _get_vqd(keywords)
    if not vqd:
        return None

    # get images
    safesearch_base = {"On": 1, "Moderate": 1, "Off": -1}

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
    while payload["s"] < min(max_results, 1000) or len(results) < max_results:
        page_data = None
        try:
            resp = SESSION.get("https://duckduckgo.com/i.js", params=payload)
            resp.raise_for_status()
            page_data = resp.json().get("results", None)
        except Exception:
            logger.exception("")
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

    results = results[:max_results]
    if output:
        _do_output(__name__, keywords, output, results)

    # download images
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
                    _download_file, res["image"], path, f"{i}_{filename}"
                )
                futures.append(future)
            for i, future in enumerate(as_completed(futures), start=1):
                logger.info("%s/%s", i, len(results))
                print(f"{i}/{len(results)}")

        print("Done.")
    return results
