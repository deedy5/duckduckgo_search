import os
import pathlib
import shutil
import time

import pytest
from click.testing import CliRunner

from duckduckgo_search import DDGS, __version__
from duckduckgo_search.cli import _download_results, _save_csv, _save_json, cli

runner = CliRunner()
TEXT_RESULTS = None
IMAGES_RESULTS = None

@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(2)


def test_version_command():
    result = runner.invoke(cli, ["version"])
    assert result.output.strip() == __version__


def test_chat_command():
    result = runner.invoke(cli, ["chat"])
    assert "chat" in result.output


def test_text_command():
    result = runner.invoke(cli, ["text", "-k", "python"])
    assert "title" in result.output


def test_images_command():
    result = runner.invoke(cli, ["images", "-k", "cat"])
    assert "title" in result.output


def test_news_command():
    result = runner.invoke(cli, ["news", "-k", "usa"])
    assert "title" in result.output


def test_videos_command():
    result = runner.invoke(cli, ["videos", "-k", "dog"])
    assert "title" in result.output


@pytest.mark.dependency()
def test_get_text():
    global TEXT_RESULTS
    TEXT_RESULTS = DDGS().text("test")
    assert TEXT_RESULTS


@pytest.mark.dependency()
def test_get_images():
    global IMAGES_RESULTS
    IMAGES_RESULTS = DDGS().images("test")
    assert IMAGES_RESULTS


@pytest.mark.dependency(depends=["test_get_data"])
def test_save_csv(tmp_path):
    temp_file = tmp_path / "test_csv.csv"
    _save_csv(temp_file, RESULTS)
    assert temp_file.exists()


@pytest.mark.dependency(depends=["test_get_data"])
def test_save_json(tmp_path):
    temp_file = tmp_path / "test_json.json"
    _save_json(temp_file, RESULTS)
    assert temp_file.exists()


@pytest.mark.dependency(depends=["test_get_data"])
def test_text_download():
    pathname = pathlib.Path("text_downloads")
    _download_results(test_text_download, TEXT_RESULTS, function_name="text", pathname=str(pathname))
    assert pathname.is_dir() and pathname.iterdir()
    for file in pathname.iterdir():
        assert file.is_file()
    shutil.rmtree(str(pathname))


@pytest.mark.dependency(depends=["test_get_images"])
def test_images_download():
    pathname = pathlib.Path("images_downloads")
    _download_results(test_images_download, IMAGES_RESULTS, function_name="images", pathname=str(pathname))
    assert pathname.is_dir() and pathname.iterdir()
    for file in pathname.iterdir():
        assert file.is_file()
    shutil.rmtree(str(pathname))
