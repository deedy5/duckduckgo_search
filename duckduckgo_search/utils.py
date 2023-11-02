import re
from html import unescape
from typing import Optional
from urllib.parse import unquote

REGEX_500_IN_URL = re.compile(r"(?:\d{3}-\d{2}\.js)")
REGEX_STRIP_TAGS = re.compile("<.*?>")

USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",  # noqa: E501
]


def _extract_vqd(html_bytes: bytes) -> Optional[str]:
    for c1, c2 in (
        (b'vqd="', b'"'),
        (b"vqd=", b"&"),
        (b"vqd='", b"'"),
    ):
        try:
            start = html_bytes.index(c1) + len(c1)
            end = html_bytes.index(c2, start)
            return html_bytes[start:end].decode()
        except ValueError:
            pass


def _is_500_in_url(url: str) -> bool:
    """something like '506-00.js' inside the url"""
    return bool(REGEX_500_IN_URL.search(url))


def _normalize(raw_html: str) -> str:
    """Strip HTML tags from the raw_html string."""
    return unescape(re.sub(REGEX_STRIP_TAGS, "", raw_html)) if raw_html else ""


def _normalize_url(url: str) -> str:
    """Unquote URL and replace spaces with '+'"""
    return unquote(url.replace(" ", "+")) if url else ""
