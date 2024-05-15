import os
import shutil
import time

import pytest
from click.testing import CliRunner

from duckduckgo_search import DDGS, __version__
from duckduckgo_search.cli import _download_results, _save_csv, _save_json, cli

runner = CliRunner()


@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(0.5)


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


def test_maps_command():
    result = runner.invoke(cli, ["maps", "-k", "school", "-p", "Berlin"])
    assert "title" in result.output


def test_answers_command():
    result = runner.invoke(cli, ["answers", "-k", "question"])
    assert "question" in result.output


def test_suggestions_command():
    result = runner.invoke(cli, ["suggestions", "-k", "sun"])
    assert "phrase" in result.output


def test_translate_command():
    result = runner.invoke(cli, ["translate", "-k", "moon", "-t", "de"])
    assert "language" in result.output


def test_save_csv(tmp_path):
    keywords = "butterfly"
    with DDGS() as ddgs:
        results = ddgs.text(keywords, max_results=30)
        assert 27 <= len(results) <= 30

    temp_file = tmp_path / f"{keywords}.csv"
    _save_csv(temp_file, results)
    assert temp_file.exists()


def test_save_json(tmp_path):
    keywords = "chicago"
    with DDGS() as ddgs:
        results = ddgs.text(keywords, max_results=30)
        assert 27 <= len(results) <= 30

    temp_file = tmp_path / f"{keywords}.json"
    _save_json(temp_file, results)
    assert temp_file.exists()


def test_text_download():
    keywords = "maradona"
    with DDGS() as ddgs:
        results = ddgs.text(keywords, max_results=8)
    assert 7 <= len(results) <= 8

    _download_results(keywords, results)

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
    with DDGS() as ddgs:
        results = ddgs.images(keywords, max_results=8)
    assert len(results) >= 8

    _download_results(keywords, results, images=True)

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
