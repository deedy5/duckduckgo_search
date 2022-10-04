import logging

import requests
from requests import ConnectionError
from typing import Optional

from .utils import SESSION, _do_output, _get_vqd, _normalize

logger = logging.getLogger(__name__)


def ddg(
    keywords: str,
    region: Optional[str] = "wt-wt",
    safesearch: Optional[str] = "Moderate",
    time: Optional[str] = None,
    max_results: Optional[int] = 25,
    output: Optional[str] = None,
    session: Optional[requests.Session] = None,
):
    """DuckDuckGo text search. Query params: https://duckduckgo.com/params

    Args:
        keywords (str): keywords for query.
        region (str, optional): country - wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): On(kp=1), Moderate(kp=-1), Off(kp=-2). Defaults to "Moderate".
        time (str, optional): 'd' (day), 'w' (week), 'm' (month), 'y' (year). Defaults to None.
        max_results (int, optional): return not less than max_results, max=200. Defaults to 25.
        output (str, optional): csv, json, print. Defaults to None.
        session (requests.Session, optional): your session for custom settings as proxies etc.

    Returns:
        Optional[List[dict]]: DuckDuckGo text search results.
    """

    if not keywords:
        return None

    # get vqd
    vqd = _get_vqd(keywords)
    if not vqd:
        return None

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
        # request search results from duckduckgo
        page_data = None
        try:
            if session is None:
                resp = SESSION.get("https://links.duckduckgo.com/d.js", params=params)
            else:
                resp = session.get("https://links.duckduckgo.com/d.js", params=params)

            logger.info(
                "%s %s %s", resp.status_code, resp.url, resp.elapsed.total_seconds()
            )
            page_data = resp.json().get("results", None)
        except ConnectionError:
            logger.error("Connection Error.")
            break
        except Exception as e:
            logger.exception(f"Exception: {e}.", exc_info=True)
            break

        if not page_data:
            break

        page_results = []
        for i, row in enumerate(page_data):

            # try pagination
            if "n" in row:
                params["s"] += i
                break

            # collect results
            if row["u"] not in cache:
                cache.add(row["u"])
                body = _normalize(row["a"])
                if body:
                    page_results.append(
                        {
                            "title": _normalize(row["t"]),
                            "href": row["u"],
                            "body": body,
                        }
                    )
        if not page_results:
            break
        results.extend(page_results)

    results = results[:max_results]
    if output:
        _do_output(__name__, keywords, output, results)
    return results
