![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg) [![](https://badgen.net/github/release/deedy5/duckduckgo_search)](https://github.com/deedy5/duckduckgo_search/releases) [![](https://badge.fury.io/py/duckduckgo-search.svg)](https://pypi.org/project/duckduckgo-search) 
## Duckduckgo_search

Search text, images, news using DuckDuckGo.com search engine 

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
