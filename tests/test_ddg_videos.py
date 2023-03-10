import os
import os.path
from random import randrange

from duckduckgo_search import ddg_videos


def test_ddg_videos():
    results = ddg_videos("cat")
    assert len(results) >= 45


def test_ddg_videos_pagination():
    results = ddg_videos("cat", page=2)
    assert len(results) >= 45


def test_ddg_videos_max_results():
    results = ddg_videos("cat", max_results=100)
    assert len(results) >= 75


def test_ddg_videos_save_csv_json():
    keywords = "cat"
    results = ddg_videos(keywords, max_results=20, output="json")
    assert len(results) >= 20
    results = ddg_videos(keywords, max_results=20, output="csv")
    assert len(results) >= 20

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_videos_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json not found")


def test_ddg_videos_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    r = ddg_videos(
        keywords=random_chars,
        region="ru-ru",
        safesearch="Off",
        time="d",
        resolution="high",
        duration="short",
        license_videos="youtube",
    )
    assert r is None
