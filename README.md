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
***Example 1. Text search***
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
***Example 2. Searching for pdf files***
```python
from duckduckgo_search import ddg

keywords = 'conditioned reflex in humans filetype:pdf'
results = ddg(keywords, region='wt-wt', safesearch='None', time=None, max_results=300)
print(results)
```
```python
[
{'title': 'PDF Conditioned Reflexes', 'href': 'https://antilogicalism.com/wp-content/uploads/2019/04/conditioned-reflexes.pdf', 'body': '302 CONDITIONED REFLEXES. in the strength of the reflexes, a state of ;affair.~ which lasted for many. days, the relation between the magnitudes of the reflexes and the Other dogs those of the inhibitable type suffered a functional disturbance of the cortical activities for a very considerable period.'},
{'title': 'Conditioned reflex therapy; the direct approach to the reconstruction...', 'href': 'https://archive.org/details/conditionedrefle00salt', 'body': "Two chapters were rewritten and expanded from the author's What is hypnosis. One was reprinted from the South west review. Bibliography: p. 321-340."},
{'title': 'conditioned reflex examples in humans - Bing', 'href': 'https://technopagan.org/conditioned+reflex+examples+in+humans&FORM=QSRE4', 'body': 'Jun 02, 2021 · Conditioned Reflex Examples In Humans And not discrimination is directly with dogs was presented is absent, and emotional responses being subtle variations in... When they hear thunder, in conditioned reflex was sent to humans are allowed early contributions ivan to know about why...'},
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

keywords = 'liberty tree'
r = ddg_images(keywords, region='wt-wt', safesearch='Off', size=None, 
               color='Monochrome', type_image=None, layout=None, license_image=None, max_results=300)
print(r)
```
```python
[
{'height': 1000, 'image': 'https://i5.walmartimages.com/asr/fef2dbdb-3756-4401-b7ae-502ec2ea082b_1.eb37ae35a5e3d4ae59d61ecac336c226.jpeg?odnWidth=1000&odnHeight=1000&odnBg=ffffff', 'source': 'Bing', 'thumbnail': 'https://tse2.mm.bing.net/th?id=OIP.4DhDDdx9IOAwbFm6CRGpTwHaHa&pid=Api', 'title': 'Liberty Tree 1765 Nthe Large Elm Tree At Boylston Market ...', 'url': 'https://www.walmart.com/ip/Liberty-Tree-1765-Nthe-Large-Elm-Tree-Boylston-Market-Boston-Massachusetts-Named-Liberty-Tree-Sons-Liberty-Held-Meetings-Summer-1765-Wood-Engraving-A/997377547?wmlspartner=bizratecom&affcmpid=3313893407&tmode=0000', 'width': 1000},
{'height': 2400, 'image': 'http://etc.usf.edu/clipart/13500/13570/liberty-tree_13570.tif', 'source': 'Bing', 'thumbnail': 'https://tse2.mm.bing.net/th?id=OIP.4t3AojTiUP6TZ-AFaSfCHAHaJ7&pid=Api', 'title': 'Liberty Tree | ClipArt ETC', 'url': 'http://etc.usf.edu/clipart/13500/13570/liberty-tree_13570.htm', 'width': 1790},
{'height': 297, 'image': 'https://www.blogtalkradio.com/api/image/resize/400x297/aHR0cHM6Ly9kYXNnN3h3bWxkaXg2LmNsb3VkZnJvbnQubmV0L2hvc3RwaWNzLzc1MGZhZjVhLTJhMTUtNDE5Ni1iOTQwLTA1NTc1NjVlMGM1MV9saWJlcnR5LXRyZWVfbG9nby5qcGc/750faf5a-2a15-4196-b940-0557565e0c51_liberty-tree_logo.jpg?mode=Fill', 'source': 'Bing', 'thumbnail': 'https://tse2.mm.bing.net/th?id=OIP.IQxgK4LaaFV82m7Iz9J3sgAAAA&pid=Api', 'title': 'Liberty Tree Radio Online Radio | BlogTalkRadio', 'url': 'http://www.blogtalkradio.com/libertytreeradio', 'width': 400},
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

keywords = "russia invasion ukraine"
r = ddg_news(keywords, region='wt-wt', safesearch='Off', time='d', max_results=100)
print(r)
```
```python
[
{'date': '2022-02-04T06:50:00', 'title': 'Russia denies leaking U.S. security talks document to El Pais', 'body': 'Moscow has demanded guarantees from Washington and NATO that Ukraine will not be allowed to join the military bloc. Russia has amassed over 100,000 troops close to the Ukrainian borders, but denies planning an invasion.', 'url': 'https://wdez.com/2022/02/04/russia-denies-leaking-u-s-security-talks-document-to-el-pais/', 'image': 'https://storage.googleapis.com/media.mwcradio.com/mimesis/2022-02/04/2022-02-04T060600Z_1_LYNXMPEI13053_RTROPTP_3_RUSSIA-USA-SECURITY.JPG', 'source': 'WDEZ'},
{'date': '2022-02-04T06:50:00', 'title': 'Analysis-Traders scour markets for protection amid Ukraine tensions', 'body': 'LONDON (Reuters) - Unnerved by the sabre-rattling between Russia and the West over Ukraine, traders are scouring ... a 10% probability of a full-fledged invasion. Ganry recommends a different ...', 'url': 'https://wsau.com/2022/02/04/analysis-traders-scour-markets-for-protection-amid-ukraine-tensions/', 'image': 'https://storage.googleapis.com/media.mwcradio.com/mimesis/2022-02/04/2022-02-04T061136Z_2_LYNXMPEI13058_RTROPTP_3_GLOBAL-MARKETS-TRADING.JPG', 'source': 'WSAY'},
{'date': '2022-02-04T06:47:00', 'title': "Morning news brief: US's warning on Russia-Ukraine crisis, Johnson's top aides quitting, and more", 'body': 'Russia will produce graphic propaganda video as pretext for an invasion against Ukraine: US © Provided by WION Pentagon officials said today that Russia could fabricate a pretext for an invasion of Ukraine. "As part of this fake attack, we believe that ...', 'url': 'https://www.msn.com/en-in/news/world/morning-news-brief-us-s-warning-on-russia-ukraine-crisis-johnson-s-top-aides-quitting-and-more/ar-AATs9ml', 'image': 'https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AATsnww.img?h=315&w=600&m=6&q=60&o=t&l=f&f=jpg', 'source': 'MSN'},
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
___
## 5. ddg_translate() - translation by duckduckgo.com

```python
from duckduckgo_search import ddg_translate

def ddg_translate(keywords, from_=None, to='en'):
    ''' DuckDuckGo translate
    keywords: string or a list of strings to translate;  
    from_: what language to translate from (defaults automatically),
    to: what language to translate (defaults to English). 
    '''
```
***Returns***
```python
[
{'detected_language': detected_language,
  'translated': translated text,
  'original': original text,},
 ...
 ]
```
***Example 1. Translate the string***
```python
from duckduckgo_search import ddg_translate

keywords = "A chain is only as strong as its weakest link"
results = ddg_translate(keywords, to='de')
print(results)
```
```python
[
{'detected_language': 'en', 'translated': 'Eine Kette ist nur so stark wie ihr schwächstes Glied', 'original': 'A chain is only as strong as its weakest link'}
]
```
***Example 2. Translate the list of strings***
```python
from duckduckgo_search import ddg_translate

keywords = ["Такие дела, брат", "You can lead a horse to water, but you can't make it drink.",
            "Ein Spatz in der Hand ist besser, als eine Taube auf dem Dach."]
results = ddg_translate(keywords, from_=None, to='tr')
print(results)
```
```python
[
{'detected_language': 'ru', 'translated': 'Böyle şeyler, kardeşim.', 'original': 'Такие дела, брат'},
{'detected_language': 'en', 'translated': 'Bir atı suya götürebilirsin ama içiremezsin.', 'original': "You can lead a horse to water, but you can't make it drink."},
{'detected_language': 'de', 'translated': 'Elinizdeki serçe çatıdaki bir güvercinden daha iyidir.', 'original': 'Ein Spatz in der Hand ist besser, als eine Taube auf dem Dach.'},
...
]
```

