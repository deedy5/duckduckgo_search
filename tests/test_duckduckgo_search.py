import os
import shutil
from itertools import islice

from duckduckgo_search import DDGS
from duckduckgo_search.cli import download_results, save_csv, save_json


def test_text():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text("cat")
        results = [x for x in islice(ddgs_gen, 25)]
        assert len(results) >= 20


def test_text_html():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text("eagle", backend="html")
        results = [x for x in islice(ddgs_gen, 25)]
        assert len(results) >= 20


def test_text_lite():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text("dog", backend="lite")
        results = [x for x in islice(ddgs_gen, 25)]
        assert len(results) >= 20


def test_images():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.images("airplane")
        results = [x for x in islice(ddgs_gen, 150)]
        assert len(results) >= 140


def test_videos():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.videos("sea")
        results = [x for x in islice(ddgs_gen, 50)]
        assert len(results) >= 40


def test_news():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.news("tesla")
        results = [x for x in islice(ddgs_gen, 40)]
        assert len(results) >= 30


def test_maps():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.maps("school", place="London")
        results = [x for x in islice(ddgs_gen, 40)]
        assert len(results) >= 30


def test_answers():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.answers("sun")
        results = [x for x in islice(ddgs_gen, 5)]
        assert len(results) >= 1


def test_suggestions():
    with DDGS() as ddgs:
        ddgs_gen = ddgs.suggestions("moon")
        results = [x for x in islice(ddgs_gen, 5)]
        assert len(results) >= 1


def test_translate():
    results = DDGS().translate("school", to="de")
    assert results == {
        "detected_language": "en",
        "translated": "Schule",
        "original": "school",
    }


def test_save_csv():
    keywords = "butterfly"
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(keywords)
        results = [x for x in islice(ddgs_gen, 25)]
        assert len(results) >= 22

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
        ddgs_gen = ddgs.text(keywords)
        results = [x for x in islice(ddgs_gen, 25)]
        assert len(results) >= 22

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
    results = [x for x in islice(DDGS().text(keywords), 10)]
    assert len(results) >= 8

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
    results = [x for x in islice(DDGS().images(keywords), 10)]
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
