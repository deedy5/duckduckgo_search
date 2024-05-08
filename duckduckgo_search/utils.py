import re
import ssl
from decimal import Decimal
from html import unescape
from math import atan2, cos, radians, sin, sqrt
from random import SystemRandom, choices
from typing import Any, Dict, List, Union
from urllib.parse import unquote

import certifi

try:
    import orjson

    ORJSON_AVAILABLE = True
except ImportError:
    import json

    ORJSON_AVAILABLE = False


from .exceptions import DuckDuckGoSearchException

CRYPTORAND = SystemRandom()
REGEX_STRIP_TAGS = re.compile("<.*?>")
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
# Include all cipher suites that Cloudflare supports today. https://developers.cloudflare.com/ssl/reference/cipher-suites/recommendations/
DEFAULT_CIPHERS = [
    "ECDHE-ECDSA-AES128-GCM-SHA256",  # modern
    "ECDHE-ECDSA-CHACHA20-POLY1305",  # modern
    "ECDHE-RSA-AES128-GCM-SHA256",  # modern
    "ECDHE-RSA-CHACHA20-POLY1305",  # modern
    "ECDHE-ECDSA-AES256-GCM-SHA384",  # modern
    "ECDHE-RSA-AES256-GCM-SHA384",  # modern
    "ECDHE-ECDSA-AES128-SHA256",  # compatible
    "ECDHE-RSA-AES128-SHA256",  # compatible
    "ECDHE-ECDSA-AES256-SHA384",  # compatible
    "ECDHE-RSA-AES256-SHA384",  # compatible
    "ECDHE-ECDSA-AES128-SHA",  # legacy
    "ECDHE-RSA-AES128-SHA",  # legacy
    "AES128-GCM-SHA256",  # legacy
    "AES128-SHA256",  # legacy
    "AES128-SHA",  # legacy
    "ECDHE-RSA-AES256-SHA",  # legacy
    "AES256-GCM-SHA384",  # legacy
    "AES256-SHA256",  # legacy
    "AES256-SHA",  # legacy
    "DES-CBC3-SHA",  # legacy
]
#
DEFAULT_HEADERS: List[Dict[str, Union[Dict[str, str], float]]] = [  # 08 may 2024
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.2833,
    },
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.1438,
    },
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.1437,
    },
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0979,
    },
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0564,
    },
    {
        "header": {
            "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0389,
    },
    {
        "header": {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-User": "document",
            "Sec-Fetch-Dest": "navigate",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0342,
    },
    {
        "header": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US;q=1.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "navigate",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-User": "document",
            "Te": "trailers",
        },
        "probability": 0.0207,
    },
    {
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0195,
    },
    {
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/124.0  Mobile/15E148 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
            "Sec-Fetch-Dest": "navigate",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-Site": "?1",
        },
        "probability": 0.0144,
    },
    {
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=1.0",
        },
        "probability": 0.0113,
    },
    {
        "header": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US;q=1.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "navigate",
            "Sec-Fetch-Mode": "same-site",
            "Sec-Fetch-Site": "?1",
            "Sec-Fetch-User": "document",
            "Te": "trailers",
        },
        "probability": 0.0105,
    },
]
HEADERS: List[Dict[str, str]] = [item["header"] for item in DEFAULT_HEADERS if isinstance(item["header"], dict)]
HEADERS_PROB: List[float] = [item["probability"] for item in DEFAULT_HEADERS if isinstance(item["probability"], float)]


def _get_headers() -> Dict[str, str]:
    """Get random headers using probability."""
    return choices(HEADERS, weights=HEADERS_PROB)[0]


def _get_ssl_context() -> ssl.SSLContext:
    """Get SSL context with shuffled ciphers."""
    shuffled_ciphers = CRYPTORAND.sample(DEFAULT_CIPHERS[6:], len(DEFAULT_CIPHERS) - 6)
    SSL_CONTEXT.set_ciphers(":".join(DEFAULT_CIPHERS[:6] + shuffled_ciphers))
    return SSL_CONTEXT


def json_dumps(obj: Any) -> str:
    try:
        return orjson.dumps(obj).decode("utf-8") if ORJSON_AVAILABLE else json.dumps(obj)
    except Exception as ex:
        raise DuckDuckGoSearchException(f"{type(ex).__name__}: {ex}") from ex


def json_loads(obj: Union[str, bytes]) -> Any:
    try:
        return orjson.loads(obj) if ORJSON_AVAILABLE else json.loads(obj)
    except Exception as ex:
        raise DuckDuckGoSearchException(f"{type(ex).__name__}: {ex}") from ex


def _extract_vqd(html_bytes: bytes, keywords: str) -> str:
    """Extract vqd from html bytes."""
    for c1, c1_len, c2 in (
        (b'vqd="', 5, b'"'),
        (b"vqd=", 4, b"&"),
        (b"vqd='", 5, b"'"),
    ):
        try:
            start = html_bytes.index(c1) + c1_len
            end = html_bytes.index(c2, start)
            return html_bytes[start:end].decode()
        except ValueError:
            pass
    raise DuckDuckGoSearchException(f"_extract_vqd() {keywords=} Could not extract vqd.")


def _text_extract_json(html_bytes: bytes, keywords: str) -> List[Dict[str, str]]:
    """text(backend="api") -> extract json from html."""
    try:
        start = html_bytes.index(b"DDG.pageLayout.load('d',") + 24
        end = html_bytes.index(b");DDG.duckbar.load(", start)
        data = html_bytes[start:end]
        result: List[Dict[str, str]] = json_loads(data)
        return result
    except Exception as ex:
        raise DuckDuckGoSearchException(f"_text_extract_json() {keywords=} {type(ex).__name__}: {ex}") from ex
    raise DuckDuckGoSearchException(f"_text_extract_json() {keywords=} return None")


def _normalize(raw_html: str) -> str:
    """Strip HTML tags from the raw_html string."""
    return unescape(REGEX_STRIP_TAGS.sub("", raw_html)) if raw_html else ""


def _normalize_url(url: str) -> str:
    """Unquote URL and replace spaces with '+'."""
    return unquote(url.replace(" ", "+")) if url else ""


def _calculate_distance(lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal) -> float:
    """Calculate distance between two points in km. Haversine formula."""
    R = 6371.0087714  # Earth's radius in km
    rlat1, rlon1, rlat2, rlon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlon, dlat = rlon2 - rlon1, rlat2 - rlat1
    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
