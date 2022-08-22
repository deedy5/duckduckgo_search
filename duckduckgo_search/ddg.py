import json
import logging
from datetime import datetime
from time import sleep

from requests import ConnectionError

from .utils import _normalize, _save_csv, _save_json, get_vqd, session

logger = logging.getLogger(__name__)


def ddg(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=28,
    output=None,
):
    """DuckDuckGo text search. Query params: https://duckduckgo.com/params

    Args:
        keywords (str): keywords for query.
        region (str, optional): country - wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): On(kp=1), Moderate(kp=-1), Off(kp=-2). Defaults to "Moderate".
        time (str, optional): 'd' (day), 'w' (week), 'm' (month), 'y' (year). Defaults to None.
        max_results (int, optional): return not less than max_results, max=200. Defaults to 28.
        output (str, optional): csv, json, print. Defaults to None.

    Returns:
        List[dict]: DuckDuckGo text search results.
    """

    if not keywords:
        return

    vqd = get_vqd(keywords)
    if not vqd:
        return
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
        # request search results from duckduckgo
        page_data = None
        try:
            resp = session.get("https://links.duckduckgo.com/d.js", params=params)
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
            try:
                # pagination
                s_param = row["n"].split("s=")[1].split("&")[0]
                params["s"] = int(s_param) - int(s_param) % 2
                break
            except Exception:
                pass

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
            results.append({
                'title': element.xpath('.//a[contains(@class, "result__a")]/text()')[0],
                'href': element.xpath('.//a[contains(@class, "result__a")]/@href')[0],
                'body': ''.join(element.xpath('.//a[contains(@class, "result__snippet")]//text()')),
            })
        if len(results) >= max_results:
            return results
        next_page = tree.xpath('.//div[@class="nav-link"]')[-1]
        names = next_page.xpath('.//input[@type="hidden"]/@name')
        values = next_page.xpath('.//input[@type="hidden"]/@value')
        payload = {n: v for n, v in zip(names, values)}
        sleep(2)
    """
    results = results[:max_results]

    # output
    keywords = keywords.replace('"', "'")
    if output == "csv":
        _save_csv(f"ddg_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.csv", results)
    elif output == "json":
        _save_json(f"ddg_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.json", results)
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=4))
            input()

    return results
