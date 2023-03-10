import os
import os.path
from random import randrange

from duckduckgo_search import ddg_news


def test_ddg_news():
    results = ddg_news("cat")
    assert len(results) >= 15


def test_ddg_news_pagination():
    results = ddg_news("cat", page=2)
    assert len(results) >= 20


def test_ddg_news_max_results():
    results = ddg_news("cat", max_results=60)
    assert len(results) >= 30


def test_ddg_news_save_csv_json():
    keywords = "cat"
    results = ddg_news(keywords, max_results=20, output="json")
    assert len(results) >= 15
    results = ddg_news(keywords, max_results=20, output="csv")
    assert len(results) >= 15

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_news_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")


# results not found
def test_ddg_news_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    results = ddg_news(
        random_chars, region="us-en", safesearch="Off", time="d",
    )
    assert results is None
