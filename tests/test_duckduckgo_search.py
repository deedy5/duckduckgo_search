import pytest

from duckduckgo_search import DDGS
from duckduckgo_search.models import MapsResult


def test_text():
    with DDGS() as ddgs:
        results = [x for x in ddgs.text("cat", max_results=30)]
        assert len(results) == 30


def test_text_params():
    with DDGS() as ddgs:
        results = [x for x in ddgs.text("cat", safesearch="off", timelimit="m", max_results=30)]
        assert len(results) == 30


def test_text_html():
    with DDGS() as ddgs:
        results = [x for x in ddgs.text("eagle", backend="html", max_results=30)]
        assert len(results) == 30


def test_text_lite():
    with DDGS() as ddgs:
        results = [x for x in ddgs.text("dog", backend="lite", max_results=30)]
        assert len(results) == 30


def test_images():
    with DDGS() as ddgs:
        results = [x for x in ddgs.images("airplane", max_results=140)]
        assert len(results) == 140


def test_videos():
    with DDGS() as ddgs:
        results = [x for x in ddgs.videos("sea", max_results=40)]
        assert len(results) == 40


def test_news():
    with DDGS() as ddgs:
        results = [x for x in ddgs.news("tesla", max_results=27)]
        assert len(results) == 27


def test_maps():
    with DDGS() as ddgs:
        results = [x for x in ddgs.maps("school", place="London", max_results=30)]
        assert len(results) == 30


def test_maps_structured_results():
    with DDGS() as ddgs:
        results = [x for x in ddgs.maps("school", place="London", max_results=30)]
        for res in results:
            MapsResult(**res)


def test_maps_raw_results():
    with DDGS() as ddgs:
        results = [x for x in ddgs.maps("school", place="London", max_results=30, raw_results=True)]
        for res in results:
            with pytest.raises(TypeError) as excinfo:
                MapsResult(**res)
            assert "unexpected keyword argument" in str(excinfo.value)


def test_answers():
    with DDGS() as ddgs:
        results = [x for x in ddgs.answers("sun")]
        assert len(results) >= 1


def test_suggestions():
    with DDGS() as ddgs:
        results = [x for x in ddgs.suggestions("moon")]
        assert len(results) >= 1


def test_translate():
    results = DDGS().translate("school", to="de")
    assert results == {
        "detected_language": "en",
        "translated": "Schule",
        "original": "school",
    }
