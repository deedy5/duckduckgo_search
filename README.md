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

### Usage
*WARNING! : The site duckduckgo.com gives an error when making frequent repeated requests.</br>
If the function returns an error, **wait 15 seconds**. </br>
Approximate time intervals depending on the number of requested results:* </br>

number of results requested | interval between requests |
---------------|---------------------------------------
1 <= max_results <=10 | 1 sec |
10 <= max_results <= 20 | 3 sec |
20 <= max_results <= 30 | 5 sec |
30 <= max_results <= 200 | >= 10 sec |



```python
from duckduckgo_search import ddg

ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30, **kwargs):
    '''
    DuckDuckGo search
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
