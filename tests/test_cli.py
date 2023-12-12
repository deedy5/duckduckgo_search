import os
import shutil

from click.testing import CliRunner

from duckduckgo_search import DDGS, __version__
from duckduckgo_search.cli import cli, download_results, save_csv, save_json

runner = CliRunner()


def test_version_command():
    result = runner.invoke(cli, ["version"])
    assert result.output.strip() == __version__


def test_text_command():
    result = runner.invoke(cli, ["text", "-k", "python"])
    assert "title" in result.output


def test_images_command():
    result = runner.invoke(cli, ["images", "-k", "cat"])
    assert "title" in result.output


def test_news_command():
    result = runner.invoke(cli, ["news", "-k", "usa"])
    assert "title" in result.output


def test_videos_command():
    result = runner.invoke(cli, ["videos", "-k", "dog"])
    assert "title" in result.output


def test_maps_command():
    result = runner.invoke(cli, ["maps", "-k", "school", "-p", "Berlin"])
    assert "title" in result.output


def test_answers_command():
    result = runner.invoke(cli, ["answers", "-k", "question"])
    assert "question" in result.output


def test_suggestions_command():
    result = runner.invoke(cli, ["suggestions", "-k", "sun"])
    assert "phrase" in result.output


def test_translate_command():
    result = runner.invoke(cli, ["translate", "-k", "moon", "-t", "de"])
    assert "language" in result.output


def test_save_csv():
    keywords = "butterfly"
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords, max_results=30)
        results = [x for x in ddgs_gen]
        assert len(results) == 30

    save_csv(f"{keywords}.csv", results)

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if keywords in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv not found")


def test_save_json():
    keywords = "chicago"
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords, max_results=30)
        results = [x for x in ddgs_gen]
        assert len(results) == 30

    save_json(f"{keywords}.json", results)

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if keywords in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("json not found")


def test_text_download():
    keywords = "maradona"
    results = [x for x in DDGS().text(keywords, max_results=8)]
    assert len(results) == 8

    download_results(keywords, results)

    # delete files contains keyword in name
    files = False
    for dir in os.listdir("."):
        if keywords in dir:
            for filename in os.listdir(dir):
                filename = f"{os.getcwd()}/{dir}/{filename}"
                if os.path.isfile(filename):
                    os.remove(filename)
                    files = True
    if not files:
        raise AssertionError("images files not found")

    # delete folder contains keyword in name
    for dir in os.listdir():
        if f"{keywords}" in dir:
            if os.path.isdir(dir):
                shutil.rmtree(dir)


def test_images_download():
    keywords = "real madrid"
    results = [x for x in DDGS().images(keywords, max_results=8)]
    assert len(results) >= 8

    download_results(keywords, results, images=True)

    # delete files contains keyword in name
    files = False
    for dir in os.listdir("."):
        if keywords in dir:
            for filename in os.listdir(dir):
                filename = f"{os.getcwd()}/{dir}/{filename}"
                if os.path.isfile(filename):
                    os.remove(filename)
                    files = True
    if not files:
        raise AssertionError("images files not found")

    # delete folder contains keyword in name
    for dir in os.listdir():
        if f"{keywords}" in dir:
            if os.path.isdir(dir):
                shutil.rmtree(dir)
