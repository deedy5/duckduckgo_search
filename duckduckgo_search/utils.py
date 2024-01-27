import json
import re
from html import unescape
from typing import Optional
from urllib.parse import unquote

from .exceptions import DuckDuckGoSearchException

REGEX_500_IN_URL = re.compile(r"(?:\d{3}-\d{2}\.js)")
REGEX_STRIP_TAGS = re.compile("<.*?>")
REGEX_VQD = re.compile(rb"""vqd=['"]?([^&"']+)""")


def _extract_vqd(html_bytes: bytes, keywords: str) -> Optional[str]:
    """Extract vqd from html using a regular expression."""
    try:
        match = REGEX_VQD.search(html_bytes)
        if match:
            return match.group(1).decode()
    except Exception:
        pass
    raise DuckDuckGoSearchException(f"_extract_vqd() {keywords=} Could not extract vqd.")


def _text_extract_json(html_bytes: bytes, keywords: str) -> Optional[str]:
    """text(backend="api") -> extract json from html."""
    try:
        start = html_bytes.index(b"DDG.pageLayout.load('d',") + 24
        end = html_bytes.index(b");DDG.duckbar.load(", start)
        data = html_bytes[start:end]
        return json.loads(data)
    except Exception as ex:
        raise DuckDuckGoSearchException(f"_text_extract_json() {keywords=} {type(ex).__name__}: {ex}") from ex


def _is_500_in_url(url: str) -> bool:
    """Something like '506-00.js' inside the url."""
    return bool(REGEX_500_IN_URL.search(url))


def _normalize(raw_html: str) -> str:
    """Strip HTML tags from the raw_html string."""
    return unescape(REGEX_STRIP_TAGS.sub("", raw_html)) if raw_html else ""


def _normalize_url(url: str) -> str:
    """Unquote URL and replace spaces with '+'."""
    return unquote(url.replace(" ", "+")) if url else ""
