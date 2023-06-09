![Python >= 3.7](https://img.shields.io/badge/python->=3.7-red.svg) [![](https://badgen.net/github/release/deedy5/duckduckgo_search)](https://github.com/deedy5/duckduckgo_search/releases) [![](https://badge.fury.io/py/duckduckgo-search.svg)](https://pypi.org/project/duckduckgo-search)
# Duckduckgo_search<a name="TOP"></a>

Search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive.

## Table of Contents
* [Install](#install)
* [CLI version](#cli-version)
* [Duckduckgo search operators](#duckduckgo-search-operators)
* [Regions](#regions)
* [Using proxy](#using-proxy)
* [1. text() - text search](#1-text---text-search-by-by-duckduckgocom)
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
ddgs text -k 'ayrton senna'
# text search via proxy (example: Tor Browser)
ddgs text -k 'china is a global threat' -p socks5://localhost:9150
# find and download pdf files
ddgs text -k "russia filetype:pdf" -m 50 -d
# find in es-es region and download pdf files via proxy (example: Tor browser)
ddgs text -k "embajada a tamorlán filetype:pdf" -r es-es -m 50 -d -p socks5://localhost:9150
# find and download xls files from a specific site
ddgs text -k 'sanctions filetype:xls site:gov.ua' -m 50 -d
# find and download any doc(x) files from a specific site
ddgs text -k 'filetype:doc site:mos.ru' -m 50 -d
# find and download images
ddgs images -k "yuri kuklachev cat theatre" -m 500 -s off -d
# find in br-br region and download images via proxy (example: Tor browser) in 10 threads
ddgs images -k 'rio carnival' -r br-br -s off -m 500 -d -th 10 -p socks5://localhost:9150
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

## Using proxy
*1. The easiest way. Launch the Tor Browser*
```python3
from duckduckgo_search import DDGS

with DDGS(proxies="socks5://localhost:9150", timeout=20) as ddgs:
    for r in ddgs.text("something you need"):
        print(r)
```
*2. Use any proxy server* (*example with [iproyal residential proxies](https://iproyal.com?r=residential_proxies)*)
```python3
from duckduckgo_search import DDGS

with DDGS(proxies="socks5://user:password@geo.iproyal.com:32325", timeout=20) as ddgs:
    for r in ddgs.text("something you need"):
        print(r)
```

[Go To TOP](#TOP)

## 1. text() - text search by duckduckgo.com
`html` and `lite` backend differ from `api`:</br>
* don't do an extra request first to get vqd,</br>
* use POST requests,</br>
* pause 0.75 seconds between paginations.</br>

If you use `html` or `lite` backend, pause at least 0.75 seconds between text() calls. 
Otherwise the site will return a 403 status code after a few requests and block your ip for a few seconds.
```python
def text(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    backend: str = "api",
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: api, html, lite. Defaults to api.
            api - collect data from https://duckduckgo.com,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
    Yields:
        dict with search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.text('live free or die', region='wt-wt', safesearch='Off', timelimit='y'):
        print(r)

# Searching for pdf files
with DDGS() as ddgs:
    for r in ddgs.text('russia filetype:pdf', region='wt-wt', safesearch='Off', timelimit='y'):
        print(r)

# Using lite backend and limit the number of results to 10
from itertools import islice

with DDGS() as ddgs:
    ddgs_gen = ddgs.text("notes from a dead house", backend="lite")
    for r in islice(ddgs_gen, 10):
        print(r)
```


[Go To TOP](#TOP)

## 2. answers() - instant answers by duckduckgo.com

```python
def answers(keywords: str) -> Iterator[Dict[str, Optional[str]]]::
    """DuckDuckGo instant answers. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.

    Yields:
        dict with instant answers results.

        """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.answers("sun"):
        print(r)
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
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo images search. Query params: https://duckduckgo.com/params

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

    Yields:
        dict with image search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'butterfly'
    ddgs_images_gen = ddgs.images(
      keywords,
      region="wt-wt",
      safesearch="Off",
      size=None,
      color="Monochrome",
      type_image=None,
      layout=None,
      license_image=None,
    )
    for r in ddgs_images_gen:
        print(r)
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
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo videos search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.

    Yields:
        dict with videos search results

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'tesla'
    ddgs_videos_gen = ddgs.videos(
      keywords,
      region="wt-wt",
      safesearch="Off",
      timelimit="w",
      resolution="high",
      duration="medium",
    )
    for r in ddgs_videos_gen:
        print(r)
```


[Go To TOP](#TOP)

## 5. news() - news search by duckduckgo.com

```python
def news(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo news search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.

    Yields:
        dict with news search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'How soon the sun will die'
    ddgs_news_gen = ddgs.news(
      keywords,
      region="wt-wt",
      safesearch="Off",
      timelimit="m",
    )
    for r in ddgs_news_gen:
        print(r)
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
    ) -> Iterator[Dict[str, Optional[str]]]:
        """DuckDuckGo maps search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query
            place: if set, the other parameters are not used. Defaults to None.
            street: house number/street. Defaults to None.
            city: city of search. Defaults to None.
            county: county of search. Defaults to None.
            state: state of search. Defaults to None.
            country: country of search. Defaults to None.
            postalcode: postalcode of search. Defaults to None.
            latitude: geographic coordinate (north–south position). Defaults to None.
            longitude: geographic coordinate (east–west position); if latitude and
                longitude are set, the other parameters are not used. Defaults to None.
            radius: expand the search square by the distance in kilometers. Defaults to 0.

        Yields:
            dict with maps search results

        """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.maps("school", place="Uganda"):
        print(r)
```

[Go To TOP](#TOP)

## 7. translate() - translation by duckduckgo.com

```python
def translate(
    self,
    keywords: str,
    from_: Optional[str] = None,
    to: str = "en",
) -> Optional[Dict[str, Optional[str]]]:
    """DuckDuckGo translate

    Args:
        keywords: string or a list of strings to translate
        from_: translate from (defaults automatically). Defaults to None.
        to: what language to translate. Defaults to "en".

    Returns:
        dict with translated keywords.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'school'
    r = ddgs.translate(keywords, to="de")
    print(r)
```

[Go To TOP](#TOP)


## 8. suggestions() - suggestions by duckduckgo.com

```python
def suggestions(
    keywords,
    region: str = "wt-wt",
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo suggestions. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

    Yields:
        dict with suggestions results.
    """
```
***Example***
```python3
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.suggestions("fly)
        print(r)
```

[Go To TOP](#TOP)
