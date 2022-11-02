import logging

from .utils import SESSION, _do_output, _get_vqd, _normalize

logger = logging.getLogger(__name__)


def ddg(
    keywords,
    region="wt-wt",
    safesearch="Moderate",
    time=None,
    max_results=25,
    output=None,
):
    """DuckDuckGo text search. Query params: https://duckduckgo.com/params

    Args:
        keywords (str): keywords for query.
        region (str, optional): country - wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): On(kp=1), Moderate(kp=-1), Off(kp=-2). Defaults to "Moderate".
        time (str, optional): 'd' (day), 'w' (week), 'm' (month), 'y' (year). Defaults to None.
        max_results (int, optional): return not less than max_results, max=200. Defaults to 25.
        output (str, optional): csv, json, print. Defaults to None.

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
    if output:
        _do_output(__name__, keywords, output, results)
    return results
