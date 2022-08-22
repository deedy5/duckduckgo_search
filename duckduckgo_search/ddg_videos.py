import json
import logging
from datetime import datetime
from time import sleep

from requests import ConnectionError

from .utils import _save_csv, _save_json, get_vqd, session

logger = logging.getLogger(__name__)


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

    Args:
        keywords: keywords for query.
        region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: On (p = 1), Moderate (p = -1), Off (p = -2). Defaults to "Moderate".
        time: d, w, m (published after). Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.
        max_results: number of results, maximum ddg_videos gives out 1000 results. Defaults to 62.
        output: csv, json, print. Defaults to None.

    Returns:
        DuckDuckGo videos search results
    """

    if not keywords:
        return

    # get vqd
    vqd = get_vqd(keywords)
    if not vqd:
        return
    sleep(0.75)

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
        page_data = None
        try:
            resp = session.get("https://duckduckgo.com/v.js", params=payload)
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
            if row["content"] not in cache:
                page_results.append(row)
                cache.add(row["content"])
        if not page_results:
            break
        results.extend(page_results)
        # for pagination
        payload["s"] += 62
        sleep(0.2)

    results = results[:max_results]

    # output
    keywords = keywords.replace('"', "'")
    if output == "csv":
        _save_csv(
            f"ddg_videos_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            results,
        )
    elif output == "json":
        _save_json(
            f"ddg_videos_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            results,
        )
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=2))
            input()

    return results
