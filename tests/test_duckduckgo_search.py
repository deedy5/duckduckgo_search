from duckduckgo_search import ddg, ddg_images, ddg_news, ddg_videos, ddg_maps


def test_ddg():
    results = ddg('cat', max_results=100)
    assert len(results) >= 70


def test_ddg_images():
    results = ddg_images('cat', max_results=100)
    assert len(results) == 100


def test_ddg_news():
    results = ddg_news('cat', max_results=100)
    assert len(results) == 100


def test_ddg_videos():
    results = ddg_videos('cat', max_results=100)
    assert len(results) == 100


def test_ddg_maps():
    results = ddg_maps('cat', place='Europe', max_results=100)
    assert len(results) == 100
