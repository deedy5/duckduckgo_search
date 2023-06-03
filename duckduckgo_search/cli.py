import asyncio
import csv
import json
import logging
import os
from datetime import datetime
from random import choice
from urllib.parse import unquote

import click
import httpx

from .duckduckgo_search import DDGS, USERAGENTS
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
    with open(jsonfile, "w") as file:
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
            click.secho(f"{i}. {'-' * 78}", bg="black", fg="white")
            for j, (k, v) in enumerate(e.items(), start=1):
                if v:
                    width = (
                        300
                        if k
                        in (
                            "content",
                            "href",
                            "image",
                            "source",
                            "thumbnail",
                            "url",
                        )
                        else 78
                    )
                    k = "language" if k == "detected_language" else k
                    text = click.wrap_text(
                        f"{v}",
                        width=width,
                        initial_indent="",
                        subsequent_indent=" " * 12,
                        preserve_paragraphs=True,
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


async def download_file(url, dir_path, filename, sem):
    headers = {"User-Agent": choice(USERAGENTS)}
    try:
        async with sem:
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", url, headers=headers) as resp:
                    if resp.status_code == 200:
                        with open(os.path.join(dir_path, filename), "wb") as file:
                            async for chunk in resp.aiter_bytes():
                                file.write(chunk)
                logger.info(f"File downloaded {url}")
    except Exception as ex:
        logger.debug(f"download_file url={url} {type(ex).__name__} {ex}")


async def _download_results(keywords, results, images=False):
    if images:
        path = f"images_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
    else:
        path = f"text_{keywords}_{datetime.now():%Y%m%d_%H%M%S}"
    os.makedirs(path, exist_ok=True)

    tasks = []
    sem = asyncio.Semaphore(20)
    for i, res in enumerate(results, start=1):
        if images:
            filename = unquote(res["image"].split("/")[-1].split("?")[0])
            task = asyncio.create_task(
                download_file(res["image"], path, f"{i}_{filename}", sem)
            )
        else:
            filename = unquote(res["href"].split("/")[-1].split("?")[0])
            task = asyncio.create_task(
                download_file(res["href"], path, f"{i}_{filename}", sem)
            )
        tasks.append(task)

    with click.progressbar(
        length=len(tasks),
        label="Downloading",
        show_percent=True,
        show_pos=True,
        width=50,
    ) as bar:
        for future in asyncio.as_completed(tasks):
            await future
            bar.update(1)

    await asyncio.gather(*tasks)


def download_results(keywords, results, images=False):
    asyncio.run(_download_results(keywords, results, images))


@click.group(chain=True)
def cli():
    pass


@cli.command()
def version():
    print(__version__)
    return __version__


@cli.command()
@click.option("-k", "--keywords", required=True, help="text search, keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="wt-wt, us-en, uk-en, ru-ru, etc. - search region https://duckduckgo.com/params",
)
@click.option(
    "-s",
    "--safesearch",
    default="moderate",
    type=click.Choice(["on", "moderate", "off"]),
    help="Safe Search",
)
@click.option(
    "-t",
    "--timelimit",
    default=None,
    type=click.Choice(["d", "w", "m", "y"]),
    help="search results for the last day, week, month, year",
)
@click.option(
    "-m",
    "--max_results",
    default=20,
    help="maximum number of results, default=20",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
@click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="download results to 'keywords' folder",
)
@click.option(
    "-b",
    "--backend",
    default="api",
    type=click.Choice(["api", "html", "lite"]),
    help="which backend to use, default=api",
)
def text(keywords, output, download, max_results, *args, **kwargs):
    data = []
    for r in DDGS().text(keywords=keywords, *args, **kwargs):
        if len(data) >= max_results:
            break
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
        download_results(keywords, data)


@cli.command()
@click.option(
    "-k", "--keywords", required=True, help="answers search, keywords for query"
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def answers(keywords, output, *args, **kwargs):
    data = []
    for r in DDGS().answers(keywords=keywords, *args, **kwargs):
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
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="wt-wt, us-en, uk-en, ru-ru, etc. - search region https://duckduckgo.com/params",
)
@click.option(
    "-s",
    "--safesearch",
    default="moderate",
    type=click.Choice(["on", "moderate", "off"]),
    help="Safe Search",
)
@click.option(
    "-t",
    "--timelimit",
    default=None,
    type=click.Choice(["Day", "Week", "Month", "Year"]),
    help="search results for the last day, week, month, year",
)
@click.option(
    "-size",
    "--size",
    default=None,
    type=click.Choice(["Small", "Medium", "Large", "Wallpaper"]),
    help="",
)
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
    "-type",
    "--type_image",
    default=None,
    type=click.Choice(["photo", "clipart", "gif", "transparent", "line"]),
)
@click.option(
    "-l", "--layout", default=None, type=click.Choice(["Square", "Tall", "Wide"])
)
@click.option(
    "-lic",
    "--license_image",
    default=None,
    type=click.Choice(["any", "Public", "Share", "Modify", "ModifyCommercially"]),
    help="""any (All Creative Commons), Public (Public Domain), Share (Free to Share and Use),
        ShareCommercially (Free to Share and Use Commercially), Modify (Free to Modify, Share,
        and Use), ModifyCommercially (Free to Modify, Share, and Use Commercially)""",
)
@click.option(
    "-m",
    "--max_results",
    default=90,
    help="maximum number of results, default=90",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
@click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="download and save images to 'keywords' folder",
)
def images(keywords, output, download, max_results, *args, **kwargs):
    data = []
    for r in DDGS().images(keywords=keywords, *args, **kwargs):
        if len(data) >= max_results:
            break
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
        download_results(keywords, data, images=True)


@cli.command()
@click.option("-k", "--keywords", required=True, help="keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="wt-wt, us-en, uk-en, ru-ru, etc. - search region https://duckduckgo.com/params",
)
@click.option(
    "-s",
    "--safesearch",
    default="moderate",
    type=click.Choice(["on", "moderate", "off"]),
    help="Safe Search",
)
@click.option(
    "-t",
    "--timelimit",
    default=None,
    type=click.Choice(["d", "w", "m"]),
    help="search results for the last day, week, month",
)
@click.option(
    "-res", "--resolution", default=None, type=click.Choice(["high", "standart"])
)
@click.option(
    "-d",
    "--duration",
    default=None,
    type=click.Choice(["short", "medium", "long"]),
)
@click.option(
    "-lic",
    "--license_videos",
    default=None,
    type=click.Choice(["creativeCommon", "youtube"]),
)
@click.option(
    "-m",
    "--max_results",
    default=50,
    help="maximum number of results, default=25",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def videos(keywords, output, max_results, *args, **kwargs):
    data = []
    for r in DDGS().videos(keywords=keywords, *args, **kwargs):
        if len(data) >= max_results:
            break
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
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="wt-wt, us-en, uk-en, ru-ru, etc. - search region https://duckduckgo.com/params",
)
@click.option(
    "-s",
    "--safesearch",
    default="moderate",
    type=click.Choice(["on", "moderate", "off"]),
    help="Safe Search",
)
@click.option(
    "-t",
    "--timelimit",
    default=None,
    type=click.Choice(["d", "w", "m", "y"]),
    help="d, w, m, y",
)
@click.option(
    "-m",
    "--max_results",
    default=25,
    help="maximum number of results, default=20",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def news(keywords, output, max_results, *args, **kwargs):
    data = []
    for r in DDGS().news(keywords=keywords, *args, **kwargs):
        if len(data) >= max_results:
            break
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
@click.option(
    "-p",
    "--place",
    default=None,
    help="simplified search - if set, the other parameters are not used",
)
@click.option("-s", "--street", default=None, help="house number/street")
@click.option("-c", "--city", default=None, help="city of search")
@click.option("-county", "--county", default=None, help="county of search")
@click.option("-state", "--state", default=None, help="state of search")
@click.option("-country", "--country", default=None, help="country of search")
@click.option("-post", "--postalcode", default=None, help="postalcode of search")
@click.option(
    "-lat",
    "--latitude",
    default=None,
    help="""geographic coordinate that specifies the north–south position,
            if latitude and longitude are set, the other parameters are not used""",
)
@click.option(
    "-lon",
    "--longitude",
    default=None,
    help="""geographic coordinate that specifies the east–west position,
            if latitude and longitude are set, the other parameters are not used""",
)
@click.option(
    "-r",
    "--radius",
    default=0,
    help="expand the search square by the distance in kilometers",
)
@click.option("-m", "--max_results", default=50, help="number of results, default=50")
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def maps(keywords, output, max_results, *args, **kwargs):
    data = []
    for i, r in enumerate(DDGS().maps(keywords=keywords, *args, **kwargs), start=1):
        if len(data) >= max_results:
            break
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
@click.option(
    "-f",
    "--from_",
    help="What language to translate from (defaults automatically)",
)
@click.option(
    "-t",
    "--to",
    default="en",
    help="de, ru, fr, etc. What language to translate, defaults='en'",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def translate(keywords, output, *args, **kwargs):
    data = DDGS().translate(keywords=keywords, *args, **kwargs)
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
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="wt-wt, us-en, uk-en, ru-ru, etc. - search region https://duckduckgo.com/params",
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv, json (save the results to a csv or json file)",
)
def suggestions(keywords, output, *args, **kwargs):
    data = []
    for r in DDGS().suggestions(keywords=keywords, *args, **kwargs):
        data.append(r)
    filename = (
        f"suggestions_{sanitize_keywords(keywords)}_{datetime.now():%Y%m%d_%H%M%S}"
    )
    if output == "print":
        print_data(data)
    elif output == "csv":
        save_csv(f"{filename}.csv", data)
    elif output == "json":
        save_json(f"{filename}.json", data)


if __name__ == "__main__":
    cli(prog_name="ddgs")
