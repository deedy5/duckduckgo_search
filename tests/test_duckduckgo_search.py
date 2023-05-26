import os
import shutil

from duckduckgo_search import DDGS
from duckduckgo_search.cli import download_results, save_csv, save_json


def test_text():
    results_gen = DDGS().text("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 25:
            break
    assert counter >= 25

def test_text_html():
    results_gen = DDGS().text("cat", backend="html")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 25:
            break
    assert counter >= 25

def test_text_lite():
    results_gen = DDGS().text("cat", backend="lite")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 25:
            break
    assert counter >= 25


def test_images():
    results_gen = DDGS().images("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 150:
            break
    assert counter >= 150


def test_videos():
    results_gen = DDGS().videos("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 40:
            break
    assert counter >= 40


def test_news():
    results_gen = DDGS().news("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 40:
            break
    assert counter >= 40


def test_maps():
    results_gen = DDGS().maps("school", place="London")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 40:
            break
    assert counter >= 40


def test_answers():
    results_gen = DDGS().answers("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 1:
            break
    assert counter >= 1


def test_suggestions():
    results_gen = DDGS().suggestions("cat")
    counter = 0
    for i, x in enumerate(results_gen):
        counter += 1
        if i >= 10:
            break
    assert counter >= 1


def test_translate():
    results = DDGS().translate("school", to="de")
    assert results == {
        "detected_language": "en",
        "translated": "Schule",
        "original": "school",
    }


def test_save_csv():
    keywords = "butterfly"
    results_gen = DDGS().text(keywords)
    results = []
    for r in results_gen:
        results.append(r)
        if len(results) >= 20:
            break
    assert len(results) >= 20

    save_csv(f"{keywords}.csv", results)
    save_json(f"{keywords}.json", results)

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
    results_gen = DDGS().text(keywords)
    results = []
    for r in results_gen:
        results.append(r)
        if len(results) >= 20:
            break
    assert len(results) >= 20

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
    results = [x for i, x in enumerate(DDGS().text(keywords)) if i <= 10]
    assert len(results) >= 10

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
    results = [x for i, x in enumerate(DDGS().images(keywords)) if i <= 10]
    assert len(results) >= 10

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
