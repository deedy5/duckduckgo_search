import json
from time import sleep
from datetime import datetime
from decimal import Decimal
from collections import deque
from dataclasses import dataclass
import requests
from lxml import html


__version__ = '1.4'


session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"}
session.headers.update(headers)



@dataclass
class MapsResult:
    ''' Dataclass for ddg_maps search results '''
    title: str = None
    address: str = None
    country_code: str = None
    latitude: str = None
    longitude: str = None
    url: str = None
    desc: str = None
    phone: str = None
    image: str = None 
    source: str = None
    links: dict = None
    hours: dict = None

        
        
def _normalize(text):
    if not text:
        return text
    body = html.fromstring(text)
    return html.tostring(body, method='text', encoding='unicode')



def ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=28):
    ''' DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year);    
    max_results = 28 gives a number of results not less than 28,   
    maximum DDG gives out about 200 results.
    '''

    # get vqd
    payload = {
        'q': keywords, 
        }    
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0].split("vqd='")[-1].split("';")[0]
    sleep(0.75)
    
    # search
    safesearch_base = {
        'On': 1, 
        'Moderate': -1, 
        'Off': -2
        }
    params = {
        'q': keywords,
        'l': region,
        'p': safesearch_base[safesearch],
        's': 0,
        'df': time,
        'o': 'json',        
        'vqd': vqd,      
        }
    results, cache = [], set()
    while len(results) < max_results and params["s"] < 200:
        resp = session.get('https://links.duckduckgo.com/d.js', params=params)
        try:
            data = resp.json()["results"]
        except:
            return results
        
        for r in data:
            try:
                s = r["n"].split("s=")[1].split('&')[0]
                params["s"] = int(s) - int(s) % 2
                break
            except:
                if r['u'] not in cache:
                    cache.add(r['u'])
                    results.append({
                        'title': _normalize(r['t']),
                        'href': r['u'],
                        'body': _normalize(r['a']),
                        })
        sleep(0.75)

    ''' using html method
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
    '''
    return results

        
    
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



def ddg_news(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30):
    ''' DuckDuckGo news search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month);    
    max_results = 30, maximum DDG_news gives out 240 results.
    '''
    
    # get vqd
    payload = {
        'q': keywords, 
        }    
    res = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(res.text)
    vqd = tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0].split("vqd='")[-1].split("';")[0]
    
    # get news
    safesearch_base = {
        'On': 1, 
        'Moderate': -1, 
        'Off': -2
        }
    params = {
        'l': region,
        'o': 'json',
        'noamp': '1',
        'q': keywords,
        'vqd': vqd,
        'p': safesearch_base[safesearch],
        'df': time,
        's': 0,
        }
    data_previous, cache = [], set()
    results = []     
    while params['s'] < min(max_results, 240):
        resp = session.get('https://duckduckgo.com/news.js', params=params)
        data = resp.json()['results']
        if data_previous and data == data_previous:
            break
        else:
            data_previous = data
        for r in data:
            title = r['title']
            if title in cache:
                continue
            else:
                cache.add(title)
            results.append({
                'date': datetime.utcfromtimestamp(r['date']).isoformat(),
                'title': title,
                'body': _normalize(r['excerpt']),
                'url': r['url'],
                'image': r.get('image', ''),
                'source': r['source'],
                 })
        params['s'] += 30
        sleep(0.2)
    return sorted(results, key=lambda x: x['date'], reverse=True)



def ddg_maps(keywords, place=None, street=None, city=None, county=None, state=None,
             country=None, postalcode=None, latitude=None, longitude=None, radius=0):
    ''' DuckDuckGo maps search
    keywords: keywords for query;
    place: simplified search - if set, the other parameters are not used;
    street: house number/street;
    city: city of search;
    county: county of search;
    state: state of search;
    country: country of search;
    postalcode: postalcode of search;
    latitude: geographic coordinate that specifies the north–south position;
    longitude: geographic coordinate that specifies the east–west position;
        if latitude and longitude are set, the other parameters are not used.
    radius: expand the search square by the distance in kilometers. 
    '''
    
    # get vqd
    payload = {
        'q': keywords, 
        }    
    resp = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(resp.text)
    vqd = tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0].split("vqd='")[-1].split("';")[0]
      
    # if longitude and latitude are specified, skip the request about bbox to the nominatim api
    if latitude and longitude:
        lat_t = Decimal(latitude.replace(',','.'))
        lat_b = Decimal(latitude.replace(',','.'))
        lon_l = Decimal(longitude.replace(',','.'))
        lon_r = Decimal(longitude.replace(',','.'))
        if radius == 0:
            radius = 1
    # otherwise request about bbox to nominatim api
    else:
        if place:
            params = {
                'q': place,
                'polygon_geojson': '0',
                'format': 'jsonv2',
                }
        else:
             params = {
                'street': street,
                'city': city,
                'county': county,
                'state': state,
                'country': country,
                'postalcode': postalcode,
                'polygon_geojson': '0',
                'format': 'jsonv2',
                }           
        resp = requests.get('https://nominatim.openstreetmap.org/search.php', params=params, headers=headers)
        coordinates = resp.json()[0]["boundingbox"]
        lat_t, lon_l = Decimal(coordinates[1]), Decimal(coordinates[2])
        lat_b, lon_r = Decimal(coordinates[0]), Decimal(coordinates[3])

    # if a radius is specified, expand the search square
    lat_t += Decimal(radius)*Decimal(0.008983)
    lat_b -= Decimal(radius)*Decimal(0.008983)
    lon_l -= Decimal(radius)*Decimal(0.008983)
    lon_r += Decimal(radius)*Decimal(0.008983)
    print(f"bbox coordinates\n{lat_t} {lon_l}\n{lat_b} {lon_r}")

    # сreate a queue of search squares (bboxes)
    work_bboxes = deque()
    work_bboxes.append((lat_t, lon_l, lat_b, lon_r))
    
    # bbox iterate
    results, cache = [], set()
    while work_bboxes:
        lat_t, lon_l, lat_b, lon_r = work_bboxes.pop()
        params = {
            'q': keywords,
            'vqd': vqd,
            'tg': 'maps_places',
            'rt': 'D',
            'mkexp': 'b',
            'wiki_info': '1',
            'is_requery': '1',
            'bbox_tl': f"{lat_t},{lon_l}",
            'bbox_br': f"{lat_b},{lon_r}",                    
            'strict_bbox': '1',
            }
        resp = session.get('https://duckduckgo.com/local.js', params=params)
        data = resp.json()["results"]
        
        for res in data:
            r = MapsResult()
            r.title = res["name"]
            r.address = res["address"]
            if r.title + r.address in cache:
                continue
            else:
                cache.add(r.title + r.address)
                r.country_code = res["country_code"]
                r.url = res["website"]
                r.phone = res["phone"]
                r.latitude = res["coordinates"]["latitude"]
                r.longitude = res["coordinates"]["longitude"]
                r.source = res["url"]
                if res["embed"]:
                    r.image = res["embed"].get("image", '')
                    r.links = res["embed"].get("third_party_links", '')
                    r.desc = res["embed"].get("description", '')
                r.hours = res["hours"]        
                results.append(r.__dict__)

        # divide the square into 4 parts and add to the queue
        if len(data) >= 15:
            lat_middle = (lat_t + lat_b) / 2
            lon_middle = (lon_l + lon_r) / 2            
            bbox1 = (lat_t, lon_l, lat_middle, lon_middle)
            bbox2 = (lat_t, lon_middle, lat_middle, lon_r)
            bbox3 = (lat_middle, lon_l, lat_b, lon_middle)
            bbox4 = (lat_middle, lon_middle, lat_b, lon_r)
            work_bboxes.extendleft([bbox1, bbox2, bbox3, bbox4])
            
        print(f"Found {len(results)}")
    return results



def ddg_translate(keywords, from_=None, to='en'):
    ''' DuckDuckGo translate
    keywords: string or a list of strings to translate;  
    from_: what language to translate from (defaults automatically),
    to: what language to translate (defaults to English). 
    '''
    
    # get vqd
    payload = {
        'q': 'translate', 
        }    
    resp = session.post("https://duckduckgo.com", data=payload)
    tree = html.fromstring(resp.text)
    vqd = tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0].split("vqd='")[-1].split("';")[0]
    
    # translate
    params = {
        'vqd': vqd,
        'query': 'translate',
        'from': from_,
        'to': to,
        }
    
    if isinstance(keywords, str):
        keywords = [keywords]
        
    results = []
    for data in keywords:
        resp = session.post('https://duckduckgo.com/translation.js', params=params, data=data.encode('utf-8'))
        result = resp.json()
        result["original"] = data
        results.append(result)
        
    return results
