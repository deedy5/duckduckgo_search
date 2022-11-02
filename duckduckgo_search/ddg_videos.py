import logging

from .utils import SESSION, _do_output, _get_vqd

logger = logging.getLogger(__name__)


def ddg_videos(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    resolution=None,
    duration=None,
    license_videos=None,
    max_results=50,
    output=None,
):
    """DuckDuckGo videos search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: On (p = 1), Moderate (p = -1), Off (p = -2). Defaults to "Moderate".
        time: d, w, m (published after). Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.
        max_results: number of results, maximum ddg_videos gives out 1000 results. Defaults to 50.
        output: csv, json, print. Defaults to None.

    Returns:
        DuckDuckGo videos search results
    """

    if not keywords:
        return None

    # get vqd
    vqd = _get_vqd(keywords)
    if not vqd:
        return None

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
    while payload["s"] < min(max_results, 1000) or len(results) < max_results:
        page_data = None
        try:
            resp = SESSION.get("https://duckduckgo.com/v.js", params=payload)
            resp.raise_for_status()
            page_data = resp.json().get("results", None)
        except Exception:
            logger.exception("")
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
        # pagination
        payload["s"] += 60

    results = results[:max_results]
    if output:
        _do_output(__name__, keywords, output, results)
    return results
