![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg) [![](https://badgen.net/github/release/deedy5/duckduckgo_search)](https://github.com/deedy5/duckduckgo_search/releases) [![](https://badge.fury.io/py/duckduckgo-search.svg)](https://pypi.org/project/duckduckgo-search) 
## Duckduckgo_search

Search text, images, news, maps using DuckDuckGo.com search engine 

***Dependencies***
```python
lxml, requests
```
***Install***
```python
pip install -U duckduckgo_search
```

# Usage

***Duckduckgo Search Operators***

| Keywords example |	Result|
| ---     | ---   |
| cats dogs |	Results about cats or dogs |
| "cats and dogs" |	Results for exact term "cats and dogs". If no results are found, related results are shown. |
| cats -dogs |	Fewer dogs in results |
| cats +dogs |	More dogs in results |
| cats filetype:pdf |	PDFs about cats. Supported file types: pdf, doc(x), xls(x), ppt(x), html |
| dogs site:example.com  |	Pages about dogs from example.com |
| cats -site:example.com |	Pages about cats, excluding example.com |
| intitle:dogs |	Page title includes the word "dogs" |
| inurl:cats  |	Page url includes the word "cats" |
___
## 1. ddg() - search by duckduckgo.com

*WARNING!*: set a delay of at least **0.75** seconds between function calls.

```python
from duckduckgo_search import ddg

def ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=28):
    ''' DuckDuckGo search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';    
    max_results = 28 gives a number of results not less than 28,   
    maximum DDG gives out about 200 results.
    '''
```
***Returns***
```python
[{'title': title of result,
  'href': href of result,
  'body': body of result,},
 {'title': title of result,
  'href': href of result,
  'body': body of result,}, ...]
```
***Example***
```python
from duckduckgo_search import ddg

keywords = 'Bella Ciao'
results = ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=28)
print(results)
```
```python
[
{'title': 'Bella Ciao - Original Italian Lyrics & English Translation ...', 'href': 'https://dailyitalianwords.com/bella-ciao-original-italian-lyrics-english-translation/', 'body': 'Bella Ciao - English Meaning (Mondine version) In the morning as soon as I get up oh goodbye beautiful, goodbye beautiful, goodbye beautiful, bye, bye, bye In the morning as soon as I get up I have to go to the paddy fields. And between insects and mosquitoes oh goodbye beautiful, goodbye beautiful, goodbye beautiful, bye, bye, bye'},
{'title': "What's the meaning of Bella Ciao | Italian song explained", 'href': 'https://www.thinkinitalian.com/bella-ciao-meaning/', 'body': "Bella Ciao is probably the most famous Italian folk song. It has been sung anywhere in the world for years, and the TV series Money Heist made it even more popular. But what does it talk about? What's the story behind its lyrics? This is a perfect chance to learn some more Italian with the meaning of Bella Ciao. Italian culture Michele"},
...
]
```
___
## 2. ddg_images() - image search by duckduckgo.com
```python
from duckduckgo_search import ddg_images

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
```
***Returns***
```python
[{'height': image height,
  'image': image url,
  'source': image source,
  'thumbnail': image thumbnail,
  'title': image title,
  'url': url where the image was found,
  'width': image width },  
 ...
 ]
```
***Example***
```python
from duckduckgo_search import ddg_images

keywords = 'world'
r = ddg_images(keywords='world', region='br-pt', safesearch='Off', time='Year', size='Wallpaper', 
               color='Green', type_image='Photo',layout='Square', license_image='Public', max_results=500)
print(r)
```
```python
[
{'height': 1920, 'image': 'https://publicdomainpictures.net/pictures/110000/velka/arid-world.jpg', 'source': 'Bing', 'thumbnail': 'https://tse4.mm.bing.net/th?id=OIP.kCgFTRlCKn04iljW31QvNQHaHa&pid=Api', 'title': 'Arid World Free Stock Photo - Public Domain Pictures', 'url': 'https://www.publicdomainpictures.net/view-image.php?image=108025&picture=arid-world', 'width': 1920},
 
{'height': 2400, 'image': 'https://www.goodfreephotos.com/albums/vector-images/kawaii-earth-vector-clipart.png', 'source': 'Bing', 'thumbnail': 'https://tse4.mm.bing.net/th?id=OIP.Sq1GMsUVFlekkoof_wwx7wHaHa&pid=Api', 'title': 'Kawaii Earth Vector Clipart image - Free stock photo ...', 'url': 'https://www.goodfreephotos.com/public-domain-images/kawaii-earth-vector-clipart.png.php', 'width': 2400},
...
]
```
___
## 3. ddg_news() - news search by duckduckgo.com
```python
from duckduckgo_search import ddg_news

def ddg_news(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30):
    ''' DuckDuckGo news search
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month);    
    max_results = 30, maximum DDG_news gives out 240 results.
    '''
```
***Returns***
```python
[{'date': datetime in isoformat,
  'title': title of result,
  'body': body of result,
  'url': url of result,
  'image': image url,
  'source': source of result, 
 ...
 ]
```
***Example***
```python
from duckduckgo_search import ddg_news

keywords = 'water'
r = ddg_images(keywords, region='it-it')
print(r)
```
```python
[
{'date': '2022-01-23T06:55:49', 'title': 'Gli stranieri di nuovo sulle vie di Francesco', 'body': 'Assisi, l&#x27;assessore Leggio: &quot;Segnali incoraggianti dalle prenotazioni internazionali per la primavera. Recuperare un mercato azzerato&quot;', 'url': 'https://www.msn.com/it-it/news/italia/gli-stranieri-di-nuovo-sulle-vie-di-francesco/ar-AAT3dMR', 'image': 'https://immagini.quotidiano.net/?url=http%3A%2F%2Fp1014p.quotidiano.net%3A80%2Fpolopoly_fs%2F1.7280413.1642920950%21%2FhttpImage%2Fimage.jpg_gen%2Fderivatives%2Ffullsize%2Fimage.jpg&w=700&h=391&mode=fill&bg=fff', 'source': 'La Nazione on MSN.com'}, 
{'date': '2022-01-23T04:40:00', 'title': "ROAD 6 GT: i nuovi pneumatici Michelin per le moto da Gran Turismo sono gia' un successo", 'body': 'I nuovi pneumatici Michelin sono stati svelati: ecco tutte le informazioni e le differenze rispetto al modello precedente', 'url': 'https://www.tecnoandroid.it/2022/01/23/road-6-gt-i-nuovi-pneumatici-michelin-per-le-moto-da-gran-turismo-sono-gia-un-successo-1022660', 'image': 'https://www.tecnoandroid.it/wp-content/uploads/2022/01/michelin-road-6-gt.jpg', 'source': 'TECNOANDROID'},
...
]
```
___
## 4. ddg_maps() - map search by duckduckgo.com
```python
from duckduckgo_search import ddg_maps

def ddg_maps(keywords, place, radius=0):
    ''' DuckDuckGo maps search
    keywords: keywords for query;  
    place: the city to search in,
    radius: expand the search square by the distance in kilometers. 
    '''
```
***Returns***
```python
[{'title': title,
  'address': address,
  'latitude': latitude,
  'longitude': longitude,
  'url': url,
  'desc': desc,
  'phone': phone,
  'image': image,             
  'source': source,
  'links': links,
  'hours': hours,}
 ...
 ]
```
***Example***
```python
from duckduckgo_search import ddg_maps

keywords = 'dentists'
place = 'Los Angeles'
r = ddg_maps(keywords, place, radius=0)
print(r)
```
```python
[
{
'title': 'Harbor Community Clinic', 
'address': '731 S Beacon St, San Pedro, CA  90731, United States', 
'latitude': 33.7372266, 
'longitude': -118.2806465, 
'url': 'https://www.harborcommunityclinic.com', 
'desc': 'Trusted Primary Care Practices serving San Pedro, CA. Contact us at 310-547-0202 or visit us at 593 W 6th St, San Pedro, CA 90731: Harbor Community Health Centers', 
'phone': '+13107325887', 
'image': 'https://sa1s3optim.patientpop.com/assets/images/provider/photos/2185353.png', 
'source': 'https://maps.apple.com/place?q=Harbor%20Community%20Clinic&auid=3544348534960817847&address=731%20S%20Beacon%20St,%20San%20Pedro,%20CA%20%2090731,%20United%20States&ll=33.7372266,-118.2806465', 
'links': {'twitter': 'https://twitter.com/harborcclinic'}, 
'hours': {'Fri': '8:30AM–5PM', 'Mon': '8:30AM–5PM', 'Thu': '8:30AM–5PM', 'Tue': '8:30AM–5PM', 'Wed': '8:30AM–5PM', 'closes_soon': 0, 'is_open': 0, 'opens_soon': 0, 'state_switch_time': '8:30AM'}
},
{
'title': 'A+ Dental', 
'address': '531 W Seventh St, San Pedro, CA  90731, United States', 
'latitude': 33.7377013677309, 
'longitude': -118.288545012474, 
'url': 'http://www.myaplusdental.com', 
'desc': 'A+ Dental & Dr. Philip W.S. Park in San Pedro CA, are commited to the most gentle family dentistry! Open Saturdays! Call us at 310-831-0003', 
'phone': '+13109844955', 
'image': 'https://static.wixstatic.com/media/5dcdb2_6bddde6197044fb58565d9216d3d518e%7Emv2.jpg/v1/fit/w_2500,h_1330,al_c/5dcdb2_6bddde6197044fb58565d9216d3d518e%7Emv2.jpg', 
'source': 'http://yelp.com/biz/pFxe1sQ5Mk9LE_L6CtcLHw', 
'links': '', 
'hours': {'Fri': '9AM–2PM', 'Mon': '9AM–6PM', 'Sat': '9AM–5PM', 'Thu': '9AM–6PM', 'Tue': '9AM–6PM', 'Wed': '9AM–6PM', 'closes_soon': 0, 'is_open': 0, 'opens_soon': 0, 'state_switch_time': '9AM'}
},
...
]
```

