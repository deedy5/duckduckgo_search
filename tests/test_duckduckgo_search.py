import time
import pytest

from duckduckgo_search import DDGS


@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(1)


def test_context_manager():
    with DDGS() as ddgs:
        results = ddgs.news("cars", max_results=30)
        assert 27 <= len(results) <= 30


def test_text():
    results = DDGS().text("cat", max_results=30)
    assert 27 <= len(results) <= 30


def test_text_params():
    results = DDGS().text("cat", safesearch="off", timelimit="m", max_results=30)
    assert 27 <= len(results) <= 30


def test_text_html():
    results = DDGS().text("eagle", backend="html", max_results=30)
    assert 27 <= len(results) <= 30


def test_text_lite():
    results = DDGS().text("dog", backend="lite", max_results=30)
    assert 27 <= len(results) <= 30


def test_images():
    results = DDGS().images("airplane", max_results=140)
    assert 135 <= len(results) <= 140


def test_videos():
    results = DDGS().videos("sea", max_results=40)
    assert 37 <= len(results) <= 40


def test_news():
    results = DDGS().news("tesla", max_results=30)
    assert 27 <= len(results) <= 30


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
