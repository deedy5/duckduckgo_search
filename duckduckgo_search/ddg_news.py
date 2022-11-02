import logging
from datetime import datetime

from .utils import SESSION, _do_output, _get_vqd, _normalize

logger = logging.getLogger(__name__)


def ddg_news(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=25,
    output=None,
):
    """DuckDuckGo news search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2). Defaults to "Moderate".
        time: 'd' (day), 'w' (week), 'm' (month). Defaults to None.
        max_results: maximum DDG_news gives out 240 results. Defaults to 25.
        output: csv, json, print. Defaults to None.

    Returns:
        DuckDuckGo news search results.
    """

    if not keywords:
        return None

    # get vqd
    vqd = _get_vqd(keywords)
    if not vqd:
        return None

    # get news
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}
    payload = {
        "l": region,
        "o": "json",
        "noamp": "1",
        "q": keywords,
        "vqd": vqd,
        "p": safesearch_base[safesearch],
        "df": time,
        "s": 0,
    }
    results, cache = [], set()
    while payload["s"] < min(max_results, 240) or len(results) < max_results:
        page_data = None
        try:
            resp = SESSION.get("https://duckduckgo.com/news.js", params=payload)
            resp.raise_for_status()
            page_data = resp.json().get("results", None)
        except Exception:
            logger.exception("")
            break

        if not page_data:
            break

        page_results = []
        for row in page_data:
            title = row["title"]
            if title not in cache:
                cache.add(title)
                page_results.append(
                    {
                        "date": datetime.utcfromtimestamp(row["date"]).isoformat(),
                        "title": title,
                        "body": _normalize(row["excerpt"]),
                        "url": row["url"],
                        "image": row.get("image", None),
                        "source": row["source"],
                    }
                )
        if not page_results:
            break
        results.extend(page_results)
        # pagination
        payload["s"] += 30

    results = sorted(results[:max_results], key=lambda x: x["date"], reverse=True)
    if output:
        _do_output(__name__, keywords, output, results)
    return results
