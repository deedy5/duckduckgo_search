import re
from html import unescape
from urllib.parse import unquote

REGEX_500_IN_URL = re.compile(r"(?:\d{3}-\d{2}\.js)")
REGEX_STRIP_TAGS = re.compile("<.*?>")

USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
]


def _is_500_in_url(url: str) -> bool:
    """something like '506-00.js' inside the url"""
    return bool(REGEX_500_IN_URL.search(url))


def _normalize(raw_html: str) -> str:
    """strip HTML tags"""
    if raw_html:
        return unescape(re.sub(REGEX_STRIP_TAGS, "", raw_html))
    return ""


def _normalize_url(url: str) -> str:
    """unquote url and replace spaces with '+'"""
    if url:
        return unquote(url).replace(" ", "+")
    return ""
