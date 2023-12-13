import json
import re
from html import unescape
from random import choice
from typing import Optional
from urllib.parse import unquote

from curl_cffi.requests import BrowserType

from .exceptions import DuckDuckGoSearchException


BROWSERS = [x.value for x in BrowserType]
REGEX_500_IN_URL = re.compile(r"(?:\d{3}-\d{2}\.js)")
REGEX_STRIP_TAGS = re.compile("<.*?>")


def _extract_vqd(html_bytes: bytes, keywords: str) -> Optional[str]:
    for c1, c2 in (
        (b'vqd="', b'"'),
        (b"vqd=", b"&"),
        (b"vqd='", b"'"),
    ):
        try:
            start = html_bytes.index(c1) + len(c1)
            end = html_bytes.index(c2, start)
            return html_bytes[start:end].decode()
        except Exception:
            pass
    raise DuckDuckGoSearchException(f"_extract_vqd() {keywords=} Could not extract vqd.")


def _text_extract_json(html_bytes: bytes, keywords: str) -> Optional[str]:
    """text(backend="api") -> extract json from html"""
    try:
        start = html_bytes.index(b"DDG.pageLayout.load('d',") + 24
        end = html_bytes.index(b");DDG.duckbar.load(", start)
        data = html_bytes[start:end]
        return json.loads(data)
    except Exception as ex:
        raise DuckDuckGoSearchException(f"_text_extract_json() {keywords=} {type(ex).__name__}: {ex}")


def _is_500_in_url(url: str) -> bool:
    """something like '506-00.js' inside the url"""
    return bool(REGEX_500_IN_URL.search(url))


def _normalize(raw_html: str) -> str:
    """Strip HTML tags from the raw_html string."""
    return unescape(re.sub(REGEX_STRIP_TAGS, "", raw_html)) if raw_html else ""


def _normalize_url(url: str) -> str:
    """Unquote URL and replace spaces with '+'"""
    return unquote(url.replace(" ", "+")) if url else ""


def _random_browser() -> BrowserType:
    """Return a random browser from the curl-cffi"""
    return choice(BROWSERS)
