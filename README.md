![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg)
## Duckduckgo

Duckduckgo.com search results.

### Dependencies
```python
lxml, requests
```
### Usage
```python
search_ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=30, **kwargs):
    '''
    DuckDuckGo search
    Query parameters, link: https://duckduckgo.com/params:
    keywords: keywords for query;
    safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
    region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
    time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';
    max_results: depends on the keyword, the maximum DDG gives out about 200 results.
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
results = search_ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=2)
print(results)
```
```python
[{'title': 'Google', 'href': 'http://www.l.google.com/', 'body': "Google has many special features to help you find exactly what you're looking for. Advertising Programs Business Solutions About Google."}, {'title': 'Google - Home | Facebook', 'href': 'https://www.facebook.com/Google/', 'body': "Google, Mountain View, CA. 28M likes · 52,285 talking about this · 611 were here. Organizing the world's information and making it universally accessible... See actions taken by the people who manage and post content. Google Inc. is responsible for this Page."}]
```
