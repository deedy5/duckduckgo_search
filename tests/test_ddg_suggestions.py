import os
import os.path
from random import randrange

from duckduckgo_search import ddg_suggestions


def test_ddg_suggestions():
    results = ddg_suggestions("cat")
    assert len(results) >= 5


def test_ddg_suggestions_save_csv_json():
    keywords = "cat"
    results = ddg_suggestions(keywords, output="json")
    assert len(results) >= 5
    results = ddg_suggestions(keywords, output="csv")
    assert len(results) >= 5

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_suggestions_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")


# results not found
def test_ddg_suggestions_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    results = ddg_suggestions(random_chars)
    assert len(results) == 0
