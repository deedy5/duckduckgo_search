import os
import os.path
import shutil
from random import randrange

from duckduckgo_search import ddg_answers


def test_ddg_answers():
    results = ddg_answers("cat", related=True)
    assert len(results) >= 5


def test_ddg_answers_save_csv_json():
    keywords = "cat"
    results = ddg_answers(keywords, related=True, output="json")
    assert len(results) >= 5
    results = ddg_answers(keywords, related=True, output="csv")
    assert len(results) >= 5

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_answers_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")


# results not found
def test_ddg_answers_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    results = ddg_answers(random_chars, related=True)
    assert len(results) == 0
