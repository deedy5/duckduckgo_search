from lxml import html
import requests

__version__ = 0.3

def ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30, **kwargs):
    '''
    DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';
    max_results: depends on the keyword, the maximum DDG gives out about 200 results.
    '''

    results, counter = [], 0
    url = 'https://html.duckduckgo.com/html'    
    safesearch_base = {'On': 1, 'Moderate': -1, 'Off': -2}
    payload = {'q': keywords, 'l': region, 'p': safesearch_base[safesearch],'df': time}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}

    while True:
        res = requests.post(url, headers=headers, data=payload)
        tree = html.fromstring(res.text)
        if tree.xpath('//div[@class="no-results"]/text()'):
            return results
        for element in tree.xpath('//div[contains(@class, "results_links")]'):
            position = {
                'title': element.xpath('.//a[contains(@class, "result__a")]/text()')[0],
                'href': element.xpath('.//a[contains(@class, "result__a")]/@href')[0],
                'body': ''.join(element.xpath('.//a[contains(@class, "result__snippet")]//text()')),
                }
            results.append(position)
            counter += 1
            if counter >= max_results:
                return results

        next_page = tree.xpath('.//div[@class="nav-link"]')[-1] 
        names = next_page.xpath('.//input[@type="hidden"]/@name')
        values = next_page.xpath('.//input[@type="hidden"]/@value')
        payload = {n: v for n, v in zip(names, values)}
