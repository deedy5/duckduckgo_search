import os
import os.path
import shutil
from random import randrange

from duckduckgo_search import ddg_images


def test_ddg_images():
    results = ddg_images("cat", max_results=50)
    assert len(results) >= 45


def test_ddg_images_save_csv_json():
    keywords = "cat"
    results = ddg_images(keywords, max_results=20, output="json")
    assert len(results) >= 20

    results = ddg_images(keywords, max_results=20, output="csv")
    assert len(results) >= 20

    # delete files contains keyword in name
    not_files = True
    for name in os.listdir():
        if f"ddg_images_{keywords}" in name:
            if os.path.isfile(name):
                os.remove(name)
                not_files = False
    if not_files:
        raise AssertionError("csv or json files not found")


def test_ddg_images_download():
    keywords = "cat"
    results = ddg_images(keywords, max_results=20, download=True)
    assert len(results) >= 20

    # delete files contains keyword in name
    files = False
    for dir in os.listdir("."):
        if f"ddg_images_{keywords}" in dir:
            for filename in os.listdir(dir):
                filename = f"{os.getcwd()}/{dir}/{filename}"
                if os.path.isfile(filename):
                    os.remove(filename)
                    files = True
    if not files:
        raise AssertionError("images files not found")

    # delete folder contains keyword in name
    for dir in os.listdir():
        if f"ddg_images_{keywords}" in dir:
            if os.path.isdir(dir):
                shutil.rmtree(dir)


def test_ddg_images_args():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(1))
    r = ddg_images(
        keywords=random_chars,
        region="us-en",
        safesearch="Off",
        size="Wallpaper",
        color="color",
        type_image="photo",
        layout="Wide",
        license_image="any",
        max_results=50,
    )
    assert len(r) > 0


def test_ddg_images_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    r = ddg_images(
        keywords=random_chars,
        region="ru-ru",
        safesearch="Off",
        size="Wallpaper",
        color="color",
        type_image="photo",
        layout="Wide",
        license_image="any",
        max_results=50,
    )
    assert len(r) == 0
