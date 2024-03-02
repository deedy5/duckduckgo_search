![Python >= 3.8](https://img.shields.io/badge/python->=3.8-red.svg) [![](https://badgen.net/github/release/deedy5/duckduckgo_search)](https://github.com/deedy5/duckduckgo_search/releases) [![](https://badge.fury.io/py/duckduckgo-search.svg)](https://pypi.org/project/duckduckgo-search) [![Downloads](https://static.pepy.tech/badge/duckduckgo-search)](https://pepy.tech/project/duckduckgo-search) [![Downloads](https://static.pepy.tech/badge/duckduckgo-search/week)](https://pepy.tech/project/duckduckgo-search)
# Duckduckgo_search v5.0b1<a name="TOP"></a>

Search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive.

**⚠️ Warning: it is better to use AsyncDDGS in asynchronous code**

:bangbang: v5.0 brings breaking changes. Try pre-release `pip install -U --pre duckduckgo_search` and test your code.

## Table of Contents
* [Install](#install)
* [CLI version](#cli-version)
* [Duckduckgo search operators](#duckduckgo-search-operators)
* [Regions](#regions)
* [DDGS and AsyncDDGS classes](#ddgs-and-asyncddgs-classes)
* [Proxies](#proxies)
* [Exceptions](#exceptions)
* [1. text() - text search](#1-text---text-search-by-duckduckgocom)
* [2. answers() - instant answers](#2-answers---instant-answers-by-duckduckgocom)
* [3. images() - image search](#3-images---image-search-by-duckduckgocom)
* [4. videos() - video search](#4-videos---video-search-by-duckduckgocom)
* [5. news() - news search](#5-news---news-search-by-duckduckgocom)
* [6. maps() - map search](#6-maps---map-search-by-duckduckgocom)
* [7. translate() - translation](#7-translate---translation-by-duckduckgocom)
* [8. suggestions() - suggestions](#8-suggestions---suggestions-by-duckduckgocom)

## Install
```python
pip install -U duckduckgo_search
```

## CLI version

```python3
ddgs --help
```
or
```python3
python -m duckduckgo_search --help
```

CLI examples:
```python3
# text search
ddgs text -k "ayrton senna"
# text search via proxy (example: Tor Browser)
ddgs text -k "china is a global threat" -p socks5://localhost:9150
# find and download pdf files
ddgs text -k "russia filetype:pdf" -m 50 -d
# find in es-es region and download pdf files via proxy (example: Tor browser)
ddgs text -k "embajada a tamorlán filetype:pdf" -r es-es -m 50 -d -p socks5://localhost:9150
# find and download xls files from a specific site
ddgs text -k "sanctions filetype:xls site:gov.ua" -m 50 -d
# find and download any doc(x) files from a specific site
ddgs text -k "filetype:doc site:mos.ru" -m 50 -d
# find and download images
ddgs images -k "yuri kuklachev cat theatre" -m 500 -s off -d
# find in br-br region and download images via proxy (example: Tor browser) in 10 threads
ddgs images -k "rio carnival" -r br-br -s off -m 500 -d -th 10 -p socks5://localhost:9150
# get latest news
ddgs news -k "ukraine war" -s off -t d -m 10
# get last day's news and save it to a csv file
ddgs news -k "hubble telescope" -t d -m 50 -o csv
# get answers and save to a json file
ddgs answers -k holocaust -o json
```
[Go To TOP](#TOP)

## Duckduckgo search operators

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

[Go To TOP](#TOP)

## Regions
<details>
  <summary>expand</summary>

    xa-ar for Arabia
    xa-en for Arabia (en)
    ar-es for Argentina
    au-en for Australia
    at-de for Austria
    be-fr for Belgium (fr)
    be-nl for Belgium (nl)
    br-pt for Brazil
    bg-bg for Bulgaria
    ca-en for Canada
    ca-fr for Canada (fr)
    ct-ca for Catalan
    cl-es for Chile
    cn-zh for China
    co-es for Colombia
    hr-hr for Croatia
    cz-cs for Czech Republic
    dk-da for Denmark
    ee-et for Estonia
    fi-fi for Finland
    fr-fr for France
    de-de for Germany
    gr-el for Greece
    hk-tzh for Hong Kong
    hu-hu for Hungary
    in-en for India
    id-id for Indonesia
    id-en for Indonesia (en)
    ie-en for Ireland
    il-he for Israel
    it-it for Italy
    jp-jp for Japan
    kr-kr for Korea
    lv-lv for Latvia
    lt-lt for Lithuania
    xl-es for Latin America
    my-ms for Malaysia
    my-en for Malaysia (en)
    mx-es for Mexico
    nl-nl for Netherlands
    nz-en for New Zealand
    no-no for Norway
    pe-es for Peru
    ph-en for Philippines
    ph-tl for Philippines (tl)
    pl-pl for Poland
    pt-pt for Portugal
    ro-ro for Romania
    ru-ru for Russia
    sg-en for Singapore
    sk-sk for Slovak Republic
    sl-sl for Slovenia
    za-en for South Africa
    es-es for Spain
    se-sv for Sweden
    ch-de for Switzerland (de)
    ch-fr for Switzerland (fr)
    ch-it for Switzerland (it)
    tw-tzh for Taiwan
    th-th for Thailand
    tr-tr for Turkey
    ua-uk for Ukraine
    uk-en for United Kingdom
    us-en for United States
    ue-es for United States (es)
    ve-es for Venezuela
    vn-vi for Vietnam
    wt-wt for No region
___
</details>

[Go To TOP](#TOP)


## DDGS and AsyncDDGS classes

The DDGS and AsyncDDGS classes are used to retrieve search results from DuckDuckGo.com.
To use the AsyncDDGS class, you can perform asynchronous operations using Python's asyncio library.
To initialize an instance of the DDGS or AsyncDDGS classes, you can provide the following optional arguments:
```python3
class DDGS:
    """DuckDuckgo_search class to get search results from duckduckgo.com

    Args:
        headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
        proxies (Union[dict, str], optional): Proxies for the HTTP client (can be dict or str). Defaults to None.
        timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
        concurrency (int):  Limit the number of concurrent requests. Defaults to 5.

    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
**:white_check_mark: If you encounter an exception with the text "Ratelimit", try decreasing the `concurrency` parameter.**

Here is an example of initializing the DDGS class. 
```python3
from duckduckgo_search import DDGS

results = DDGS().text("python programming", max_results=5)
print(results)

# You can use DDGS also as context manager
with DDGS() as ddgs:
    results = ddgs.text("python programming", max_results=5)
    print(results)
```
Here is an example of initializing the AsyncDDGS class:
```python3
import asyncio
import logging
import sys

from duckduckgo_search import AsyncDDGS

# bypass curl-cffi NotImplementedError in windows https://curl-cffi.readthedocs.io/en/latest/faq/
if sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def aget_results(word):
    addgs = AsyncDDGS(proxies=None)
    results = await addgs.text(word, max_results=100)
    return results

# You can use AsyncDDGS also as context manager
async def aget_results(word):
    async with AsyncDDGS(proxies=None) as addgs:
        results = await addgs.text(word, max_results=100)
        return results

# reduce concurrency limit to avoid Ratelimit exceptions
async def aget_results(word):
    results = await AsyncDDGS(concurrency=2).text(word, max_results=100)
    return results

async def main():
    words = ["sun", "earth", "moon"]
    tasks = [aget_results(w) for w in words]
    results = await asyncio.gather(*tasks)
    print(results)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
```

[Go To TOP](#TOP)

## Proxies
Proxy can be specified as a dictionary or just a string
```python
proxies = {"http": "socks5://localhost:9150", "https": "socks5://localhost:9150"}
proxies = "socks5://localhost:9150"
```

*1. The easiest way. Launch the Tor Browser*
```python3
from duckduckgo_search import DDGS

ddgs = DDGS(proxies="socks5://localhost:9150", timeout=20)
results = ddgs.text("something you need", max_results=50)
```
*2. Use any proxy server* (*example with [iproyal residential proxies](https://iproyal.com?r=residential_proxies)*)
```python3
from duckduckgo_search import DDGS

ddgs = DDGS(proxies="socks5://user:password@geo.iproyal.com:32325", timeout=20)
results = ddgs.text("something you need", max_results=50)
```

[Go To TOP](#TOP)

## Exceptions

Exceptions:
- `DuckDuckGoSearchException`: Raised when there is a generic exception during the API request.
  
[Go To TOP](#TOP)

## 1. text() - text search by duckduckgo.com

```python
def text(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    backend: str = "api",
    max_results: Optional[int] = None,
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params.

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: api, html, lite. Defaults to api.
            api - collect data from https://duckduckgo.com,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with search results, or None if there was an error.

    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().text('live free or die', region='wt-wt', safesearch='off', timelimit='y', max_results=10)

# Searching for pdf files
results = DDGS().text('russia filetype:pdf', region='wt-wt', safesearch='off', timelimit='y', max_results=10)

# async
results = await AsyncDDGS().text('sun', region='wt-wt', safesearch='off', timelimit='y', max_results=10)
```

[Go To TOP](#TOP)

## 2. answers() - instant answers by duckduckgo.com

```python
def answers(keywords: str) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo instant answers. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query,
    
    Returns:
        List of dictionaries with instant answers results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().answers("sun")

# async
results = await AsyncDDGS().answers("sun")
```

[Go To TOP](#TOP)

## 3. images() - image search by duckduckgo.com

```python
def images(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    type_image: Optional[str] = None,
    layout: Optional[str] = None,
    license_image: Optional[str] = None,
    max_results: Optional[int] = None,
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo images search. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper. Defaults to None.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
        type_image: photo, clipart, gif, transparent, line.
            Defaults to None.
        layout: Square, Tall, Wide. Defaults to None.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
    Returns:
        List of dictionaries with images search results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().images(
    keywords="butterfly",
    region="wt-wt",
    safesearch="off",
    size=None,
    color="Monochrome",
    type_image=None,
    layout=None,
    license_image=None,
    max_results=100,
)

# async
results = await AsyncDDGS().images('sun', region='wt-wt', safesearch='off', max_results=20)
```

[Go To TOP](#TOP)

## 4. videos() - video search by duckduckgo.com

```python
def videos(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    resolution: Optional[str] = None,
    duration: Optional[str] = None,
    license_videos: Optional[str] = None,
    max_results: Optional[int] = None,
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo videos search. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
    Returns:
        List of dictionaries with videos search results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().videos(
    keywords="cars",
    region="wt-wt",
    safesearch="off",
    timelimit="w",
    resolution="high",
    duration="medium",
    max_results=100,
)

# async
results = await AsyncDDGS().videos('sun', region='wt-wt', safesearch='off', timelimit='y', max_results=10)
```

[Go To TOP](#TOP)

## 5. news() - news search by duckduckgo.com

```python
def news(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    max_results: Optional[int] = None,
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo news search. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
    Returns:
        List of dictionaries with news search results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().news(keywords="sun", region="wt-wt", safesearch="off", timelimit="m", max_results=20)

# async
results = await AsyncDDGS().news('sun', region='wt-wt', safesearch='off', timelimit='d', max_results=10)
```

[Go To TOP](#TOP)

## 6. maps() - map search by duckduckgo.com

```python
def maps(
    keywords,
    place: Optional[str] = None,
    street: Optional[str] = None,
    city: Optional[str] = None,
    county: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    postalcode: Optional[str] = None,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    radius: int = 0,
    max_results: Optional[int] = None,
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo maps search. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query
        place: if set, the other parameters are not used. Defaults to None.
        street: house number/street. Defaults to None.
        city: city of search. Defaults to None.
        county: county of search. Defaults to None.
        state: state of search. Defaults to None.
        country: country of search. Defaults to None.
        postalcode: postalcode of search. Defaults to None.
        latitude: geographic coordinate (north-south position). Defaults to None.
        longitude: geographic coordinate (east-west position); if latitude and
            longitude are set, the other parameters are not used. Defaults to None.
        radius: expand the search square by the distance in kilometers. Defaults to 0.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.
    
    Returns:
        List of dictionaries with maps search results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

results = DDGS().maps("school", place="Uganda", max_results=50)

# async
results = await AsyncDDGS().maps('shop', place="Baltimor", max_results=10)
```

[Go To TOP](#TOP)

## 7. translate() - translation by duckduckgo.com

```python
def translate(
    self,
    keywords: str,
    from_: Optional[str] = None,
    to: str = "en",
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo translate.
    
    Args:
        keywords: string or list of strings to translate.
        from_: translate from (defaults automatically). Defaults to None.
        to: what language to translate. Defaults to "en".
    
    Returns:
        List od dictionaries with translated keywords, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

keywords = 'school'
# also valid
keywords = ['school', 'cat']
results = DDGS().translate(keywords, to="de")

# async
results = await AsyncDDGS().translate('sun', to="de")
```

[Go To TOP](#TOP)

## 8. suggestions() - suggestions by duckduckgo.com

```python
def suggestions(
    keywords,
    region: str = "wt-wt",
) -> Optional[List[Dict[str, Optional[str]]]]:
    """DuckDuckGo suggestions. Query params: https://duckduckgo.com/params.
    
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
    
    Returns:
        List of dictionaries with suggestions results, or None if there was an error.
    
    Raises:
        DuckDuckGoSearchException: Raised when there is a generic exception during the API request.
    """
```
***Example***
```python3
from duckduckgo_search import DDGS

results = DDGS().suggestions("fly")

# async
results = await AsyncDDGS().suggestions('sun')
```

[Go To TOP](#TOP)
