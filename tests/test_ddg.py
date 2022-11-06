import os
import os.path
import shutil
from random import randrange

from duckduckgo_search import ddg


def test_ddg():
    results = ddg("cat", max_results=50)
    assert len(results) >= 45


def test_ddg_save_csv_json():
    keywords = "cat"
    results = ddg(keywords, max_results=20, output="json")
    assert len(results) >= 20
    results = ddg(keywords, max_results=20, output="csv")
    assert len(results) >= 20

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
    results = ddg(keywords, max_results=10, download=True)
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


# results not found
def test_ddg_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    results = ddg(random_chars, safesearch="Off", time="d", max_results=50)
    assert len(results) == 0
