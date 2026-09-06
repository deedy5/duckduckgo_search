"""You.com text search engine (Web Search API)."""

import json
import logging
import os
from typing import Any, ClassVar

from ddgs.base import BaseSearchEngine
from ddgs.exceptions import RatelimitException
from ddgs.results import TextResult

logger = logging.getLogger(__name__)


def _youcom_api_key() -> str | None:
    """Read the You.com API key from the environment (`YDC_API_KEY`)."""
    return os.environ.get("YDC_API_KEY")


class Youcom(BaseSearchEngine[TextResult]):
    """You.com text search engine.

    Uses the You.com Web Search API (`POST https://ydc-index.io/v1/search`), which returns
    structured JSON instead of a scraped results page. Requires an API key, read from the
    `YDC_API_KEY` environment variable (get one at https://you.com/platform/api-keys).
    The engine is disabled unless a key is present, so it never joins `auto`/`all` rotation
    for users who have not configured it.
    """

    disabled: ClassVar[bool] = _youcom_api_key() is None

    name = "you"
    category = "text"
    provider = "you"
    priority = 1.5

    search_url = "https://ydc-index.io/v1/search"
    search_method = "POST"

    # DDGS uses on/moderate/off; the You.com API uses off/moderate/strict
    # (moderate is the API default). Map `on` -> `strict` so the caller's
    # choice is not silently weakened to the API default.
    SAFESEARCH_MAP: ClassVar[dict[str, str]] = {
        "on": "strict",
        "moderate": "moderate",
        "off": "off",
    }

    def build_payload(
        self,
        query: str,
        region: str,
        safesearch: str,
        timelimit: str | None,
        page: int = 1,  # noqa: ARG002
        **kwargs: str,  # noqa: ARG002
    ) -> dict[str, Any]:
        """Build a payload for the You.com search request."""
        payload: dict[str, Any] = {"query": query, "count": 20}
        if mapped_safesearch := self.SAFESEARCH_MAP.get(safesearch):
            payload["safesearch"] = mapped_safesearch
        if country := region.lower().split("-", 1)[0]:
            payload["country"] = country.upper()
        if timelimit:
            payload["freshness"] = {"d": "day", "w": "week", "m": "month", "y": "year"}.get(timelimit, timelimit)
        return payload

    def search(
        self,
        query: str,
        region: str = "us-en",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        page: int = 1,
        **kwargs: str,  # noqa: ARG002
    ) -> list[TextResult] | None:
        """Search the You.com Web Search API."""
        api_key = _youcom_api_key()
        if not api_key:
            logger.warning("You.com engine: YDC_API_KEY is not set; skipping.")
            return None
        payload = self.build_payload(query=query, region=region, safesearch=safesearch, timelimit=timelimit, page=page)
        resp = self.http_client.request(
            "POST",
            self.search_url,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code == 429:
            msg = f"You.com engine: HTTP {resp.status_code} (rate limit)."
            raise RatelimitException(msg)
        if resp.status_code != 200:
            logger.warning("You.com engine: HTTP %s, body: %s", resp.status_code, resp.text[:200])
            return None
        return self.extract_results(resp.text)

    def extract_results(self, html_text: str) -> list[TextResult]:
        """Extract search results from the You.com JSON response.

        The response contains a `results` object with `web` (and, for news-intent queries,
        `news`) arrays. Each item has `title`, `url`, `description`, and `snippets`.
        """
        json_data = json.loads(html_text)
        sections = json_data.get("results", {})
        items = [*sections.get("web", []), *sections.get("news", [])]
        results = []
        for item in items:
            snippets = item.get("snippets") or []
            result = TextResult()
            result.title = item.get("title", "")
            result.href = item.get("url", "")
            result.body = snippets[0] if snippets else (item.get("description", "") or "")
            results.append(result)
        return results
