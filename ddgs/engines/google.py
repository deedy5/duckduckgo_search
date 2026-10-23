"""Google search engine implementation."""

from collections.abc import Mapping
from random import SystemRandom
from typing import Any, ClassVar

from ddgs.base import BaseSearchEngine
from ddgs.results import TextResult

random = SystemRandom()


def get_ua() -> str:
    """Return one User-Agent string."""
    firmware = random.choice(("2.0617.1.0.3", "2.0625.2.0.2", "2.0635.2.0.2", "5.0706.4.0.1", "5.0819.4.0.1"))
    ua = f"NokiaN72/{firmware} Series60/2.8 Profile/MIDP-2.0 Configuration/CLDC-1.1"
    if random.choice((True, False)):
        uc_version = random.choice(("7.9.1.120", "7.9.1.121", "7.9.1.122"))
        ua += f"/UC Browser{uc_version}/27/351/UCWEB"
    return ua


class Google(BaseSearchEngine[TextResult]):
    """Google search engine."""

    disabled = True  # !!!

    name = "google"
    category = "text"
    provider = "google"

    search_url = "https://www.google.com/wml/search"
    search_method = "GET"
    headers_update: ClassVar[dict[str, str]] = {"User-Agent": get_ua()}

    items_xpath = "//div[./div[1]/a and ./div[2][table]]"
    elements_xpath: ClassVar[Mapping[str, str]] = {
        "title": "./div[a]/a/span[1]/text()",
        "href": "./div[a]/a/@href",
        "body": "./div[2][table]//text()",
    }

    def build_payload(
        self,
        query: str,
        region: str,
        safesearch: str,
        timelimit: str | None,
        page: int = 1,
        **kwargs: str,  # noqa: ARG002
    ) -> dict[str, Any]:
        """Build a payload for the Google search request."""
        self.http_client.client.set_cookies("google.com", {"CONSENT": "YES+"})
        safesearch_base = {"on": "2", "moderate": "1", "off": "0"}
        start = (page - 1) * 10
        payload = {
            "q": query,
            "sca_esv": "1",
            "filter": safesearch_base[safesearch.lower()],
            "start": str(start),
        }
        country, lang = region.split("-")
        payload["hl"] = f"{lang}-{country.upper()}"  # interface language
        payload["lr"] = f"lang_{lang}"  # restricts to results written in a particular language
        payload["cr"] = f"country{country.upper()}"  # restricts to results written in a particular country
        if timelimit:
            payload["tbs"] = f"qdr:{timelimit}"
        return payload

    def pre_process_html(self, html_text: str) -> str:
        """Pre-process html_text before extracting results."""
        return html_text[html_text.find("?>") :]

    def post_extract_results(self, results: list[TextResult]) -> list[TextResult]:
        """Post-process search results."""
        post_results = []
        for result in results:
            if result.href.startswith("/url?q="):
                result.href = result.href.split("?q=")[1].split("&")[0].split("?")[0]
            if result.title and result.href.startswith("http"):
                post_results.append(result)
        return post_results
