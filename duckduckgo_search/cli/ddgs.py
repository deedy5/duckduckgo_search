import click

from duckduckgo_search import (
    __version__,
    ddg,
    ddg_answers,
    ddg_images,
    ddg_maps,
    ddg_news,
    ddg_translate,
    ddg_videos,
)


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


def print_data(data):
    if data:
        for i, e in enumerate(data, start=1):
            click.secho(f"{i}. {'-' * 78}", bg="black", fg="white")
            for j, (k, v) in enumerate(e.items(), start=1):
                if v:
                    text = click.wrap_text(
                        f"{v}",
                        width=78,
                        initial_indent="",
                        subsequent_indent=" " * 12,
                        preserve_paragraphs=True,
                    )
                else:
                    text = v
                click.secho(f"{k:<12}{text}", bg="black", fg=COLORS[j], overline=True)
            input()


@click.group(chain=True)
def cli():
    pass


@cli.command()
def version():
    print(__version__)
    return __version__


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
    help="maximum number of results, max=200.",
)
@click.option("-o", "--output", default="print", help="csv or json, default=print")
@click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="download and save documents to 'keywords' folder, default=False",
)
def text(output, *args, **kwargs):
    data = ddg(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


@cli.command()
@click.option("-k", "--keywords", help="answers search, keywords for query")
@click.option(
    "-rt", "--related", default=False, is_flag=True, help="Add related topics"
)
@click.option("-o", "--output", default="print", help="csv or json, default=print")
def answers(output, *args, **kwargs):
    data = ddg_answers(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


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
    "-m", "--max_results", default=100, help="maximum number of results, max=1000"
)
@click.option(
    "-o",
    "--output",
    default="print",
    help="csv or json, default=print",
)
@click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="download and save images to 'keywords' folder, default=False",
)
def images(output, *args, **kwargs):
    data = ddg_images(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


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
@click.option(
    "-m", "--max_results", default=50, help="maximum number of results, max=1000"
)
@click.option("-o", "--output", default="print", help="csv or json, default=print")
def videos(output, *args, **kwargs):
    data = ddg_videos(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


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
@click.option(
    "-m", "--max_results", default=25, help="maximum number of results, max=240"
)
@click.option("-o", "--output", default="print", help="csv or json, default=print")
def news(output, *args, **kwargs):
    data = ddg_news(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


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
@click.option("-o", "--output", default="print", help="csv or json, default=print")
def maps(output, *args, **kwargs):
    data = ddg_maps(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


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
@click.option("-o", "--output", default="print", help="csv or json, default=print")
def translate(output, *args, **kwargs):
    data = ddg_translate(output=output, *args, **kwargs)
    if output == "print":
        print_data(data)


if __name__ == "__main__":
    cli(prog_name="ddgs")
