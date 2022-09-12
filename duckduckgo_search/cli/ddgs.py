import click

from duckduckgo_search import (
    ddg,
    ddg_images,
    ddg_maps,
    ddg_news,
    ddg_translate,
    ddg_videos,
)


@click.group(chain=True)
def cli():
    pass


@cli.command()
@click.option("-k", "--keywords", help="text search, keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",
)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m, y")
@click.option(
    "-m",
    "--max_results",
    default=25,
    help="number of results (not less than 25), maximum DDG gives out about 200 results",
)
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
def text(*args, **kwargs):
    return ddg(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",
)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="Day, Week, Month, Year")
@click.option("-size", "--size", default=None, help="Small, Medium, Large, Wallpaper")
@click.option(
    "-c",
    "--color",
    default=None,
    help="""color, Monochrome, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Black, Gray,
            Teal, White""",
)
@click.option(
    "-type", "--type_image", default=None, help="photo, clipart, gif, transparent, line"
)
@click.option("-l", "--layout", default=None, help="Square, Tall, Wide")
@click.option(
    "-lic",
    "--license_image",
    default=None,
    help="""any (All Creative Commons), Public (Public Domain), Share (Free to Share and Use),
        ShareCommercially (Free to Share and Use Commercially), Modify (Free to Modify, Share,
        and Use), ModifyCommercially (Free to Modify, Share, and Use Commercially)""",
)
@click.option(
    "-m", "--max_results", default=100, help="number of results (default=100)"
)
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
@click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="download and save images to 'keywords' folder, default=False",
)
def images(*args, **kwargs):
    return ddg_images(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",
)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m (published after)")
@click.option("-res", "--resolution", default=None, help="high, standart")
@click.option(
    "-d",
    "--duration",
    default=None,
    help="short, medium, long",
)
@click.option(
    "-lic",
    "--license_videos",
    default=None,
    help="creativeCommon, youtube",
)
@click.option("-m", "--max_results", default=50, help="number of results (default=50)")
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
def videos(*args, **kwargs):
    return ddg_videos(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
@click.option(
    "-r",
    "--region",
    default="wt-wt",
    help="country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.",
)
@click.option("-s", "--safesearch", default="Moderate", help="On, Moderate, Off")
@click.option("-t", "--time", default=None, help="d, w, m, y")
@click.option("-m", "--max_results", default=25, help="number of results (default=25)")
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
def news(*args, **kwargs):
    return ddg_news(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="keywords for query")
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
@click.option("-m", "--max_results", help="number of results (default=None)")
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
def maps(*args, **kwargs):
    return ddg_maps(*args, **kwargs)


@cli.command()
@click.option("-k", "--keywords", help="text for translation")
@click.option(
    "-f",
    "--from_",
    help="de, ru, fr, etc. What language to translate from (defaults automatically)",
)
@click.option(
    "-t",
    "--to",
    default="en",
    help="de, ru, fr, etc. What language to translate (defaults='en')",
)
@click.option("-o", "--output", default="print", help="print, csv, json, default=print")
def translate(*args, **kwargs):
    return ddg_translate(*args, **kwargs)


if __name__ == "__main__":
    cli(prog_name="ddgs")
