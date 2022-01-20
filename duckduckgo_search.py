import json
from time import sleep
import requests
from lxml import html


__version__ = 0.9


session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"})


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


        
def ddg_images(keywords, region='wt-wt', safesearch='Moderate', time=None, size=None,
               color=None, type_image=None, layout=None, license_image=None, max_results=100):
    ''' DuckDuckGo images search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: Day, Week, Month, Year;
    size: Small, Medium, Large, Wallpaper;
    color: color, Monochrome, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Black, Gray, Teal, White;
    type_image: photo, clipart, gif, transparent, line;
    layout: Square, Tall, Wide;
    license_image: any (All Creative Commons), Public (Public Domain), Share (Free to Share and Use),
             ShareCommercially (Free to Share and Use Commercially), Modify (Free to Modify, Share, and Use),
             ModifyCommercially (Free to Modify, Share, and Use Commercially);
    max_results: number of results, maximum ddg_images gives out 1000 results.
    '''
    
    # get vqd
    payload = {
        'q': keywords, 
        }    
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0].split("vqd='")[-1].split("';")[0]

    # get images
    safesearch_base = {
        'On': 1, 
        'Moderate': -1, 
        'Off': -2
        }

    time = f"time:{time}" if time else ''
    size = f"size:{size}" if size else ''
    color = f"color:{color}" if color else ''
    type_image = f"type:{type_image}" if type_image else ''
    layout = f"layout:{layout}" if layout else ''
    license_image = f"license:{license_image}" if license_image else ''    
    payload = { 
        'l': region,
        'o': 'json',
        's': 0,
        'q': keywords,
        'vqd': vqd,
        'f': f"{time},{size},{color},{type_image},{layout},{license_image}",
        'p': safesearch_base[safesearch]
        }

    results = []     
    while payload['s'] < max_results:
        res = session.get("https://duckduckgo.com/i.js", params=payload)
        data = res.json()
        results.extend(r for r in data['results'])
        payload['s'] += 100
    return results
    
