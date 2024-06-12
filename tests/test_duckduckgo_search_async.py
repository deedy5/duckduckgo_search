import time
import pytest

from duckduckgo_search import AsyncDDGS


@pytest.fixture(autouse=True)
def pause_between_tests():
    time.sleep(0.5)

@pytest.mark.asyncio
async def test_context_manager():
    async with AsyncDDGS() as addgs:
        results = await addgs.anews("cars", max_results=30)
        assert 20 <= len(results) <= 30


@pytest.mark.asyncio
@pytest.mark.parametrize("model", ["gpt-3.5", "claude-3-haiku", "llama-3-70b", "mixtral-8x7b"])
async def test_chat(model):
    results = await AsyncDDGS().achat("cat", model=model)
    assert  len(results) >= 1


@pytest.mark.asyncio
async def test_text():
    results = await AsyncDDGS().atext("sky", safesearch="off", timelimit="m", max_results=30)
    assert 27 <= len(results) <= 30


@pytest.mark.asyncio
async def test_text_html():
    results = await AsyncDDGS().atext("eagle", backend="html", max_results=30)
    assert 27 <= len(results) <= 30


@pytest.mark.asyncio
async def test_text_lite():
    results = await AsyncDDGS().atext("dog", backend="lite", max_results=30)
    assert 27 <= len(results) <= 30


@pytest.mark.asyncio
async def test_async_images():
    results = await AsyncDDGS().aimages("flower", max_results=200)
    assert 95 <= len(results) <= 200


@pytest.mark.asyncio
async def test_async_videos():
    results = await AsyncDDGS().avideos("sea", max_results=40)
    assert 37 <= len(results) <= 40


@pytest.mark.asyncio
async def test_async_news():
    results = await AsyncDDGS().anews("tesla", max_results=30)
    assert 20 <= len(results) <= 30


@pytest.mark.asyncio
async def test_async_maps():
    results = await AsyncDDGS().amaps("school", place="London", max_results=30)
    assert 27 <= len(results) <= 30


@pytest.mark.asyncio
async def test_answers():
    results = await AsyncDDGS().aanswers("sun")
    assert len(results) >= 1


@pytest.mark.asyncio
async def test_suggestions():
    results = await AsyncDDGS().asuggestions("moon")
    assert len(results) >= 1


@pytest.mark.asyncio
async def test_async_translate():
    results = await AsyncDDGS().atranslate(["school", "tomatoes"], to="de")
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