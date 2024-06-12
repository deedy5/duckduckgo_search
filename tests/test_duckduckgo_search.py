import time
import pytest

from duckduckgo_search import DDGS


@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(0.5)


def test_context_manager():
    with DDGS() as ddgs:
        results = ddgs.news("cars", max_results=30)
        assert 20 <= len(results) <= 30


@pytest.mark.parametrize("model", ["gpt-3.5", "claude-3-haiku", "llama-3-70b", "mixtral-8x7b"])
def test_chat(model):
    results = DDGS().chat("cat", model=model)
    assert  len(results) >= 1


def test_text():
    results = DDGS().text("cat", safesearch="off", timelimit="m", max_results=30)
    assert 27 <= len(results) <= 30


def test_text_html():
    results = DDGS().text("eagle", backend="html", max_results=30)
    assert 27 <= len(results) <= 30


def test_text_lite():
    results = DDGS().text("dog", backend="lite", max_results=30)
    assert 27 <= len(results) <= 30


def test_images():
    results = DDGS().images("flower", max_results=200)
    assert 95 <= len(results) <= 200


def test_videos():
    results = DDGS().videos("sea", max_results=40)
    assert 37 <= len(results) <= 40


def test_news():
    results = DDGS().news("tesla", max_results=30)
    assert 20 <= len(results) <= 30


def test_maps():
    results = DDGS().maps("school", place="London", max_results=30)
    assert 27 <= len(results) <= 30


def test_answers():
    results = DDGS().answers("sun")
    assert len(results) >= 1


def test_suggestions():
    results = DDGS().suggestions("moon")
    assert len(results) >= 1


def test_translate():
    results = DDGS().translate(["school", "tomatoes"], to="de")
    expected_results = [
        {
            "detected_language": "en",
            "translated": "Schule",
            "original": "school",
        },
        {
            "detected_language": "en",
            "translated": "Tomaten",
            "original": "tomatoes",
        }
    ]
    assert all(er in results for er in expected_results)
