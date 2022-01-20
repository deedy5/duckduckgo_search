![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg) [![](https://badgen.net/github/release/deedy5/duckduckgo_search)](https://github.com/deedy5/duckduckgo_search/releases) [![](https://badge.fury.io/py/duckduckgo-search.svg)](https://pypi.org/project/duckduckgo-search) 
## Duckduckgo_search

Duckduckgo.com search results.

### Dependencies
```python
lxml, requests
```
### Install
```python
pip install -U duckduckgo_search
```

# Usage

## 1. ddg() - search by duckduckgo.com

*WARNING!*: set the delay between function calls to **2 seconds** to avoid site error. </br>
If the function returns an error, wait 15 seconds. </br>

```python
from duckduckgo_search import ddg

ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30, **kwargs):
    ''' DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';    
    max_results = 30 gives a number of results not less than 30,   
    maximum DDG gives out about 200 results.
    '''
```
### Returns
```python
[{'title': title of result,
  'href': href of result,
  'body': body of result,},
 {'title': title of result,
  'href': href of result,
  'body': body of result,}, ...]
```
### Example
```python
from duckduckgo_search import ddg

keywords = 'google'
results = ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=2)
print(results)
```
```python
[
 {
 'title': 'Google', 
 'href': 'http://www.l.google.com/', 
 'body': "Google has many special features to help you find exactly what you're looking for. Advertising Programs Business Solutions About Google."
 }, 
 {
 'title': 'Google - Home | Facebook', 
 'href': 'https://www.facebook.com/Google/', 
 'body': "Google, Mountain View, CA. 28M likes · 52,285 talking about this · 611 were here. Organizing the world's information and making it universally accessible... See actions taken by the people who manage and post content. Google Inc. is responsible for this Page."
 },
]
```
___
## 2. ddg_images() - image search by duckduckgo.com
```python
from duckduckgo_search import ddg_images

ddg_images(keywords, region='wt-wt', safesearch='Moderate', time=None, size=None,
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
### Returns
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
### Example
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
