from random import randrange

from duckduckgo_search import ddg_maps


def test_ddg_maps():
    results = ddg_maps("school", place="Europe", max_results=50)
    assert len(results) == 50


# if results not found
def test_ddg_maps_not_results():
    random_chars = "".join(chr(randrange(65, 90)) for i in range(100))
    r = ddg_maps(keywords=random_chars, place="United States", max_results=50)
    assert len(r) == 0
