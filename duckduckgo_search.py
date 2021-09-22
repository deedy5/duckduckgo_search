from time import sleep
from lxml import html
import requests

__version__ = 0.7

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"})

def ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30, **kwargs):
    ''' DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';    
    max_results = 30 gives a number of results not less than 30,   
    maximum DDG gives out about 200 results.
    '''
    
    safesearch_base = {
        'On': 1, 
        'Moderate': -1, 
        'Off': -2
        }
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
            results.append({'title': element.xpath('.//a[contains(@class, "result__a")]/text()')[0],
                            'href': element.xpath('.//a[contains(@class, "result__a")]/@href')[0],
                            'body': ''.join(element.xpath('.//a[contains(@class, "result__snippet")]//text()')),})
        if len(results) >= max_results:
            return results

        next_page = tree.xpath('.//div[@class="nav-link"]')[-1] 
        names = next_page.xpath('.//input[@type="hidden"]/@name')
        values = next_page.xpath('.//input[@type="hidden"]/@value')
        payload = {n: v for n, v in zip(names, values)}
        sleep(2)
