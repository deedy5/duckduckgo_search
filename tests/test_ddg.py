import os
import os.path
import shutil
from random import randrange

from duckduckgo_search import ddg


def test_ddg():
    results = ddg("cat")
    assert len(results) >= 15


def test_ddg_pagination():
    results = ddg("cat", page=2)
    assert len(results) >= 15


def test_ddg_max_results():
    results = ddg("cat", max_results=50)
    assert len(results) >= 35


def test_ddg_save_csv_json():
    keywords = "cat"
    results = ddg(keywords, output="json")
    assert len(results) >= 15
    results = ddg(keywords, output="csv")
    assert len(results) >= 15

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")


def test_ddg_download():
    keywords = "cat"
    results = ddg(keywords, download=True)
    assert len(results) >= 10

    # delete files contains keyword in name
    files = False
    for dir in os.listdir("."):
        if f"ddg_{keywords}" in dir:
            for filename in os.listdir(dir):
                filename = f"{os.getcwd()}/{dir}/{filename}"
                if os.path.isfile(filename):
                    os.remove(filename)
                    files = True
    if not files:
        raise AssertionError("Files not found")

    # delete folder contains keyword in name
    for dir in os.listdir():
        if f"ddg_{keywords}" in dir:
            if os.path.isdir(dir):
                shutil.rmtree(dir)
