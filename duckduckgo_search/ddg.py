import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .utils import SESSION, _do_output, _download_file, _get_vqd, _normalize

logger = logging.getLogger(__name__)


def ddg(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=25,
    output=None,
    download=False,
):
    """DuckDuckGo text search. Query params: https://duckduckgo.com/params

    Args:
        keywords (str): keywords for query.
        region (str, optional): wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): On, Moderate, Off. Defaults to "Moderate".
        time (Optional[str], optional): d, w, m, y. Defaults to None.
        max_results (int, optional): maximum number of results, max=200. Defaults to 25.
        output (Optional[str], optional): csv, json. Defaults to None.
        download (bool, optional): if True, download and save dociments to 'keywords' folder.
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

    # search
    safesearch_base = {"On": 1, "Moderate": -1, "Off": -2}
    payload = {
        "q": keywords,
        "l": region,
        "p": safesearch_base[safesearch],
        "s": 0,
        "df": time,
        "o": "json",
        "vqd": vqd,
    }

    results, cache = [], set()
    while payload["s"] < min(max_results, 200) or len(results) < max_results:
        # request search results from duckduckgo
        page_data = None
        try:
            resp = SESSION.get("https://links.duckduckgo.com/d.js", params=payload)
            resp.raise_for_status()
            page_data = resp.json().get("results", None)
        except Exception:
            logger.exception("")
            break

        if not page_data:
            break

        page_results = []
        for i, row in enumerate(page_data):

            # try pagination
            if "n" in row:
                payload["s"] += i
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

    """ using html method
    payload = {
        'q': keywords,
        'l': region,
        'p': safesearch_base[safesearch],
        'df': time
        }
    results = []
    while True:
        res = SESSION.post('https://html.duckduckgo.com/html', data=payload, **kwargs)
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
    keywords = keywords.replace(" filetype:", "_")
    if output:
        _do_output(__name__, keywords, output, results)

    # download documents
    if download:
        print("Downloading documents. Wait...")
        keywords = keywords.replace('"', "'")
        path = f"ddg_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
        os.makedirs(path, exist_ok=True)
        futures = []
        with ThreadPoolExecutor(30) as executor:
            for i, res in enumerate(results, start=1):
                filename = res["href"].split("/")[-1].split("?")[0]
                future = executor.submit(
                    _download_file, res["href"], path, f"{i}_{filename}"
                )
                futures.append(future)
            for i, future in enumerate(as_completed(futures), start=1):
                logger.info("%s/%s", i, len(results))
                print(f"{i}/{len(results)}")

        print("Done.")
    return results
