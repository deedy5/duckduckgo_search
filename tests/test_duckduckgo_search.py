import time
import pytest

from duckduckgo_search import DDGS


@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(2)


def test_context_manager():
    with DDGS() as ddgs:
        results = ddgs.news("cars", max_results=30)
        assert 20 <= len(results) <= 30


@pytest.mark.parametrize("model", ["gpt-4o-mini", "llama-3.3-70b", "claude-3-haiku", "o3-mini", "mistral-small-3"])
def test_chat(model):
    results = DDGS().chat("cat", model=model)
    assert  len(results) >= 1


def test_text_html():
    results = DDGS().text("eagle", backend="html", region="br-pt", timelimit="y", max_results=20)
    assert 15 <= len(results) <= 20


def test_text_lite():
    results = DDGS().text("dog", backend="lite", region="br-pt", timelimit="y", max_results=20)
    assert 15 <= len(results) <= 20


def test_images():
    results = DDGS().images("flower", max_results=200)
    assert 85 <= len(results) <= 200


def test_videos():
    results = DDGS().videos("sea", max_results=40)
    assert 30 <= len(results) <= 40


def test_news():
    results = DDGS().news("tesla", max_results=30)
    assert 20 <= len(results) <= 30
