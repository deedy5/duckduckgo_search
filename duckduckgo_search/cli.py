import csv
import json
import logging
import os
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from urllib.parse import unquote

import click
from curl_cffi import requests

from .duckduckgo_search import DDGS
from .utils import _random_browser
from .version import __version__

logger = logging.getLogger(__name__)

COLORS = {
    0: "black",
    1: "red",
    2: "green",
    3: "yellow",
    4: "blue",
    5: "magenta",
    6: "cyan",
    7: "bright_black",
    8: "bright_red",
    9: "bright_green",
    10: "bright_yellow",
    11: "bright_blue",
    12: "bright_magenta",
    13: "bright_cyan",
}


def save_json(jsonfile, data):
    with open(jsonfile, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_csv(csvfile, data):
    with open(csvfile, "w", newline="", encoding="utf-8") as file:
        if data:
            headers = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(data)


def print_data(data):
    if data:
        for i, e in enumerate(data, start=1):
            click.secho(f"{i}.\t    {'=' * 78}", bg="black", fg="white")
            for j, (k, v) in enumerate(e.items(), start=1):
                if v:
                    width = 300 if k in ("content", "href", "image", "source", "thumbnail", "url") else 78
                    k = "language" if k == "detected_language" else k
                    text = click.wrap_text(
                        f"{v}", width=width, initial_indent="", subsequent_indent=" " * 12, preserve_paragraphs=True
                    )
                else:
                    text = v
                click.secho(f"{k:<12}{text}", bg="black", fg=COLORS[j], overline=True)
            input()


def sanitize_keywords(keywords):
    keywords = (
        keywords.replace("filetype", "")
        .replace(":", "")
        .replace('"', "'")
        .replace("site", "")
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "")
    )
    return keywords


def download_file(url, dir_path, filename, proxy):
    try:
        resp = requests.get(url, proxies=proxy, impersonate=_random_browser(), timeout=10)
        resp.raise_for_status()
        with open(os.path.join(dir_path, filename[:200]), "wb") as file:
            file.write(resp.content)
    except Exception as ex:
        logger.debug(f"download_file url={url} {type(ex).__name__} {ex}")


def download_results(keywords, results, images=False, proxy=None, threads=None):
    path_type = "images" if images else "text"
    path = f"{path_type}_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
    os.makedirs(path, exist_ok=True)
    proxy = {"http": proxy, "https": proxy}

    threads = 10 if threads is None else threads
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for i, res in enumerate(results, start=1):
            url = res["image"] if images else res["href"]
            filename = unquote(url.split("/")[-1].split("?")[0])
            f = executor.submit(download_file, url, path, f"{i}_{filename}", proxy)
            futures.append(f)

        with click.progressbar(
            length=len(futures), label="Downloading", show_percent=True, show_pos=True, width=50
        ) as bar:
            for future in as_completed(futures):
                future.result()
                bar.update(1)


@click.group(chain=True)
def cli():
    pass


@cli.command()
def version():
    print(__version__)
    return __version__


@cli.command()
@click.option("-k", "--keywords", required=True, help="text search, keywords for query")
@click.option("-r", "--region", default="wt-wt", help="wt-wt, us-en, ru-ru, etc. -region https://duckduckgo.com/params")
@click.option("-s", "--safesearch", default="moderate", type=click.Choice(["on", "moderate", "off"]))
@click.option("-t", "--timelimit", default=None, type=click.Choice(["d", "w", "m", "y"]), help="day, week, month, year")
@click.option("-m", "--max_results", default=20, help="maximum number of results, default=20")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-d", "--download", is_flag=True, default=False, help="download results to 'keywords' folder")
@click.option("-b", "--backend", default="api", type=click.Choice(["api", "html", "lite"]), help="which backend to use")
@click.option("-th", "--threads", default=10, help="download threads, default=10")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def text(keywords, region, safesearch, timelimit, backend, output, download, threads, max_results, proxy):
    data = []
    for r in DDGS(proxies=proxy).text(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        backend=backend,
        max_results=max_results,
    ):
        data.append(r)
    keywords = sanitize_keywords(keywords)
    filename = f"text_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print" and not download:
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)
    if download:
        download_results(keywords, data, proxy=proxy, threads=threads)


@cli.command()
@click.option("-k", "--keywords", required=True, help="answers search, keywords for query")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def answers(keywords, output, proxy, *args, **kwargs):
    data = []
    for r in DDGS(proxies=proxy).answers(keywords=keywords, *args, **kwargs):
        data.append(r)
    filename = f"answers_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option("-r", "--region", default="wt-wt", help="wt-wt, us-en, ru-ru, etc. -region https://duckduckgo.com/params")
@click.option("-s", "--safesearch", default="moderate", type=click.Choice(["on", "moderate", "off"]))
@click.option("-t", "--timelimit", default=None, type=click.Choice(["Day", "Week", "Month", "Year"]))
@click.option("-size", "--size", default=None, type=click.Choice(["Small", "Medium", "Large", "Wallpaper"]))
@click.option(
    "-c",
    "--color",
    default=None,
    type=click.Choice(
        [
            "color",
            "Monochrome",
            "Red",
            "Orange",
            "Yellow",
            "Green",
            "Blue",
            "Purple",
            "Pink",
            "Brown",
            "Black",
            "Gray",
            "Teal",
            "White",
        ]
    ),
)
@click.option(
    "-type", "--type_image", default=None, type=click.Choice(["photo", "clipart", "gif", "transparent", "line"])
)
@click.option("-l", "--layout", default=None, type=click.Choice(["Square", "Tall", "Wide"]))
@click.option(
    "-lic",
    "--license_image",
    default=None,
    type=click.Choice(["any", "Public", "Share", "Modify", "ModifyCommercially"]),
)
@click.option("-m", "--max_results", default=90, help="maximum number of results, default=90")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-d", "--download", is_flag=True, default=False, help="download and save images to 'keywords' folder")
@click.option("-th", "--threads", default=10, help="download threads, default=10")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def images(
    keywords,
    region,
    safesearch,
    timelimit,
    size,
    color,
    type_image,
    layout,
    license_image,
    download,
    threads,
    max_results,
    output,
    proxy,
):
    data = []
    for r in DDGS(proxies=proxy).images(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
        license_image=license_image,
        max_results=max_results,
    ):
        data.append(r)
    keywords = sanitize_keywords(keywords)
    filename = f"images_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print" and not download:
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)
    if download:
        download_results(keywords, data, images=True, proxy=proxy, threads=threads)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option("-r", "--region", default="wt-wt", help="wt-wt, us-en, ru-ru, etc. -region https://duckduckgo.com/params")
@click.option("-s", "--safesearch", default="moderate", type=click.Choice(["on", "moderate", "off"]))
@click.option("-t", "--timelimit", default=None, type=click.Choice(["d", "w", "m"]), help="day, week, month")
@click.option("-res", "--resolution", default=None, type=click.Choice(["high", "standart"]))
@click.option("-d", "--duration", default=None, type=click.Choice(["short", "medium", "long"]))
@click.option("-lic", "--license_videos", default=None, type=click.Choice(["creativeCommon", "youtube"]))
@click.option("-m", "--max_results", default=50, help="maximum number of results, default=50")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def videos(keywords, output, max_results, proxy, *args, **kwargs):
    data = []
    for r in DDGS(proxies=proxy).videos(keywords=keywords, *args, **kwargs):
        data.append(r)
    filename = f"videos_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option("-r", "--region", default="wt-wt", help="wt-wt, us-en, ru-ru, etc. -region https://duckduckgo.com/params")
@click.option("-s", "--safesearch", default="moderate", type=click.Choice(["on", "moderate", "off"]))
@click.option("-t", "--timelimit", default=None, type=click.Choice(["d", "w", "m", "y"]), help="day, week, month, year")
@click.option("-m", "--max_results", default=25, help="maximum number of results, default=25")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def news(keywords, output, max_results, proxy, *args, **kwargs):
    data = []
    for r in DDGS(proxies=proxy).news(keywords=keywords, *args, **kwargs):
        data.append(r)
    filename = f"news_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option("-p", "--place", default=None, help="simplified search - if set, the other parameters are not used")
@click.option("-s", "--street", default=None, help="house number/street")
@click.option("-c", "--city", default=None, help="city of search")
@click.option("-county", "--county", default=None, help="county of search")
@click.option("-state", "--state", default=None, help="state of search")
@click.option("-country", "--country", default=None, help="country of search")
@click.option("-post", "--postalcode", default=None, help="postalcode of search")
@click.option("-lat", "--latitude", default=None, help="""if lat and long are set, the other params are not used""")
@click.option("-lon", "--longitude", default=None, help="""if lat and long are set, the other params are not used""")
@click.option("-r", "--radius", default=0, help="expand the search square by the distance in kilometers")
@click.option("-m", "--max_results", default=50, help="number of results, default=50")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-proxy", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def maps(keywords, output, max_results, proxy, *args, **kwargs):
    data = []
    for i, r in enumerate(DDGS(proxies=proxy).maps(keywords=keywords, *args, **kwargs), start=1):
        data.append(r)
        if i % 100 == 0:
            print(i)
    filename = f"maps_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


@cli.command()
@click.option("-k", "--keywords", required=True, help="text for translation")
@click.option("-f", "--from_", help="What language to translate from (defaults automatically)")
@click.option("-t", "--to", default="en", help="de, ru, fr, etc. What language to translate, defaults='en'")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def translate(keywords, output, proxy, *args, **kwargs):
    data = DDGS(proxies=proxy).translate(keywords=keywords, *args, **kwargs)
    data = [data]
    filename = f"translate_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option("-r", "--region", default="wt-wt", help="wt-wt, us-en, ru-ru, etc. -region https://duckduckgo.com/params")
@click.option("-o", "--output", default="print", help="csv, json (save the results to a csv or json file)")
@click.option("-p", "--proxy", help="the proxy to send requests, example: socks5://localhost:9150")
def suggestions(keywords, output, proxy, *args, **kwargs):
    data = []
    for r in DDGS(proxies=proxy).suggestions(keywords=keywords, *args, **kwargs):
        data.append(r)
    filename = f"suggestions_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


if __name__ == "__main__":
    cli(prog_name="ddgs")
