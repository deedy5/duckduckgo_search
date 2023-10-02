import logging
import warnings

from .duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


# deprecated, for compatibility
def ddg(
    keywords, region="wt-wt", safesearch="moderate", time=None, max_results=None, page=1, output=None, download=False
):
    warnings.warn("ddg is deprecated. Use DDGS().text() generator")
    results = []
    for r in DDGS().text(
        keywords=keywords, region=region, safesearch=safesearch, timelimit=time, max_results=max_results
    ):
        results.append(r)
        if page and len(results) >= 20:
            break
    return results


# deprecated, for compatibility
def ddg_images(
    keywords,
    region="wt-wt",
    safesearch="moderate",
    time=None,
    size=None,
    color=None,
    type_image=None,
    layout=None,
    license_image=None,
    max_results=None,
    page=1,
    output=None,
    download=False,
):
    warnings.warn("ddg_images is deprecated. Use DDGS().images() generator")
    results = []
    for r in DDGS().images(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=time,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
        license_image=license_image,
        max_results=max_results,
    ):
        results.append(r)
        if page and len(results) >= 90:
            break
    return results


# deprecated, for compatibility
def ddg_videos(
    keywords,
    region="wt-wt",
    safesearch="moderate",
    time=None,
    resolution=None,
    duration=None,
    license_videos=None,
    max_results=None,
    page=1,
    output=None,
):
    warnings.warn("ddg_videos is deprecated. Use DDGS().videos() generator")
    results = []
    for r in DDGS().videos(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=time,
        resolution=resolution,
        duration=duration,
        license_videos=license_videos,
        max_results=max_results,
    ):
        results.append(r)
        if page and len(results) >= 50:
            break
    return results


# deprecated, for compatibility
def ddg_news(keywords, region="wt-wt", safesearch="moderate", time=None, max_results=None, page=1, output=None):
    warnings.warn("ddg_news is deprecated. Use DDGS().news() generator")
    results = []
    for r in DDGS().news(
        keywords=keywords, region=region, safesearch=safesearch, timelimit=time, max_results=max_results
    ):
        results.append(r)
        if page and len(results) >= 25:
            break
    return results


# deprecated, for compatibility
def ddg_maps(
    keywords,
    place=None,
    street=None,
    city=None,
    county=None,
    state=None,
    country=None,
    postalcode=None,
    latitude=None,
    longitude=None,
    radius=0,
    max_results=None,
    output=None,
):
    warnings.warn("ddg_maps is deprecated. Use DDGS().maps() generator")
    results = []
    for r in DDGS().maps(
        keywords=keywords,
        place=place,
        street=street,
        city=city,
        county=county,
        state=state,
        country=country,
        postalcode=postalcode,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        max_results=max_results,
    ):
        results.append(r)
        if len(results) >= 100:
            break
    return results


# deprecated, for compatibility
def ddg_answers(keywords, related=False, output=None):
    warnings.warn("ddg_answers is deprecated. Use DDGS().answers() generator")
    results = []
    for r in DDGS().answers(keywords=keywords):
        results.append(r)
        if len(results) >= 1:
            break
    return results


# deprecated, for compatibility
def ddg_suggestions(keywords, region="wt-wt", output=None):
    warnings.warn("ddg_suggestions is deprecated. Use DDGS().suggestions() generator")
    results = []
    for r in DDGS().suggestions(keywords=keywords, region=region):
        results.append(r)
        if len(results) >= 10:
            break
    return results


# deprecated, for compatibility
def ddg_translate(keywords, from_=None, to="en", output=None):
    warnings.warn("ddg_translate is deprecated. Use DDGS().translate()")
    results = DDGS().translate(keywords=keywords, from_=from_, to=to)
    return results
