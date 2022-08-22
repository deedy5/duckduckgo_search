import os
import os.path

from duckduckgo_search import ddg_translate


def test_ddg_translate_str():
    results = ddg_translate("school", to="de")
    assert results == [
        {"detected_language": "en", "translated": "Schule", "original": "school"}
    ]


def test_ddg_translate_list_str():
    results = ddg_translate(["school", "salt"], to="de")
    assert results == [
        {"detected_language": "en", "translated": "Schule", "original": "school"},
        {"detected_language": "en", "translated": "Salz", "original": "salt"},
    ]


def test_ddg_translate_save_csv_json():
    keywords = "cat"
    results = ddg_translate(keywords, to="de", output="json")
    assert len(results) == 1
    results = ddg_translate(keywords, to="de", output="csv")
    assert len(results) == 1

    # delete files and folders contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_translate_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")
