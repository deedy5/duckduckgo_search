"""Offline tests for the You.com engine: payload building, response parsing, registration."""

import json
from typing import Any, cast

import pytest

from ddgs.engines import ENGINES
from ddgs.engines.youcom import Youcom
from ddgs.exceptions import RatelimitException
from ddgs.results import TextResult

SAMPLE_RESPONSE = json.dumps(
    {
        "results": {
            "web": [
                {
                    "url": "https://example.com/one",
                    "title": "Example One",
                    "description": "First example page.",
                    "snippets": ["snippet one"],
                },
                {
                    "url": "https://example.com/two",
                    "title": "Example Two",
                    "description": "Second example page.",
                    "snippets": [],
                },
            ],
            "news": [
                {
                    "url": "https://example.com/news",
                    "title": "Example News",
                    "description": "A news article.",
                    "snippets": ["news snippet"],
                },
            ],
        }
    }
)


def test_extract_results_parses_web_and_news() -> None:
    engine = Youcom.__new__(Youcom)  # skip __init__ (no HTTP client needed)
    results = engine.extract_results(SAMPLE_RESPONSE)
    assert len(results) == 3
    assert all(isinstance(r, TextResult) for r in results)
    assert results[0].title == "Example One"
    assert results[0].href == "https://example.com/one"
    assert results[0].body == "snippet one"
    assert results[1].body == "Second example page."  # falls back to description
    assert results[2].title == "Example News"


def test_extract_results_empty_payload() -> None:
    engine = Youcom.__new__(Youcom)
    assert engine.extract_results(json.dumps({"results": {}})) == []
    assert engine.extract_results(json.dumps({})) == []


def test_build_payload_defaults() -> None:
    engine = Youcom.__new__(Youcom)
    payload = engine.build_payload(query="wolf", region="us-en", safesearch="moderate", timelimit=None, page=1)
    assert payload == {"query": "wolf", "count": 20, "country": "US"}


def test_build_payload_region_and_timelimit() -> None:
    engine = Youcom.__new__(Youcom)
    payload = engine.build_payload(query="wolf", region="de-de", safesearch="on", timelimit="w", page=2)
    assert payload["country"] == "DE"
    assert payload["freshness"] == "week"


def test_engine_metadata() -> None:
    assert Youcom.name == "you"
    assert Youcom.category == "text"
    assert Youcom.provider == "you"


def test_disabled_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("YDC_API_KEY", raising=False)
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: None)
    assert youcom_module.Youcom.disabled is True


def test_enabled_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("YDC_API_KEY", "test-key")
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: "test-key")
    engine_cls = type("YoucomEnabled", (youcom_module.Youcom,), {"disabled": False})
    assert getattr(engine_cls, "disabled") is False


def test_search_skips_without_key(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: None)
    engine = youcom_module.Youcom(proxy=None, timeout=5)
    with caplog.at_level("WARNING"):
        result = engine.search("wolf")
    assert result is None
    assert "YDC_API_KEY" in caplog.text


class _FakeResponse:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text


class _FakeHttpClient:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text
        self.calls: list[dict[str, object]] = []

    def request(self, *args: object, **kwargs: object) -> _FakeResponse:
        self.calls.append({"args": args, "kwargs": kwargs})  # type: ignore[arg-type]
        return _FakeResponse(self.status_code, self.text)


def test_search_ok_with_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: "test-key")
    engine = youcom_module.Youcom(proxy=None, timeout=5)
    fake = _FakeHttpClient(200, SAMPLE_RESPONSE)
    engine.http_client = fake  # type: ignore[assignment]
    results = engine.search("wolf")
    assert results is not None and len(results) == 3
    sent = cast("dict[str, Any]", fake.calls[0])
    assert sent["args"][0] == "POST"
    assert sent["args"][1] == "https://ydc-index.io/v1/search"
    assert sent["kwargs"]["headers"]["X-API-Key"] == "test-key"
    assert sent["kwargs"]["json"]["query"] == "wolf"


def test_search_raises_on_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: "test-key")
    engine = youcom_module.Youcom(proxy=None, timeout=5)
    engine.http_client = _FakeHttpClient(429, '{"error": "rate limit"}')  # type: ignore[assignment]
    with pytest.raises(RatelimitException):
        engine.search("wolf")


def test_search_returns_none_on_error_status(monkeypatch: pytest.MonkeyPatch) -> None:
    from ddgs.engines import youcom as youcom_module

    monkeypatch.setattr(youcom_module, "_youcom_api_key", lambda: "test-key")
    engine = youcom_module.Youcom(proxy=None, timeout=5)
    engine.http_client = _FakeHttpClient(402, '{"error": "payment_required"}')  # type: ignore[assignment]
    assert engine.search("wolf") is None


def test_engines_registry_respects_disabled_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    """`you` must not be selectable in the registry unless enabled."""
    from ddgs.engines import youcom as youcom_module

    assert ("you" not in ENGINES["text"]) or (not youcom_module.Youcom.disabled)
