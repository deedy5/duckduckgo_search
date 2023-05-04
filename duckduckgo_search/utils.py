import csv
import json
import logging
import os
import re
from datetime import datetime
from html import unescape
from shutil import copyfileobj
from time import sleep

import requests
from diskcache import Cache

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Referer": "https://duckduckgo.com/",
}
HEADERS_FILE_DOWNLOAD = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
}
SESSION = requests.Session()
SESSION.headers = HEADERS
RE_STRIP_TAGS = re.compile("<.*?>")
try:
    VQD_CACHE = Cache(
        f"{os.path.dirname(__file__)}/vqd_cache",
        size_limit=104_857_600,
        eviction_policy="least-frequently-used",
    )
except OSError:
    VQD_CACHE = Cache(
        "vqd_cache", size_limit=104_857_600, eviction_policy="least-frequently-used"
    )


def _get_vqd(keywords):
    global SESSION

    vqd_bytes = VQD_CACHE.get(keywords, None)
    if vqd_bytes:
        logger.debug("keywords=%s. Got vqd from cache", keywords)
        return vqd_bytes.decode()

    payload = {"q": keywords}
    for _ in range(2):
        try:
            resp = SESSION.post("https://duckduckgo.com", data=payload, timeout=10)
            resp.raise_for_status()
            vqd_index_start = resp.content.index(b"vqd='") + 5
            vqd_index_end = resp.content.index(b"'", vqd_index_start)
            vqd_bytes = resp.content[vqd_index_start:vqd_index_end]

            if vqd_bytes:
                VQD_CACHE[keywords] = vqd_bytes
                return vqd_bytes.decode()

        except Exception:
            logger.exception("")

        # refresh SESSION if not vqd
        prev_proxies = SESSION.proxies
        SESSION = requests.Session()
        SESSION.headers = HEADERS
        SESSION.proxies = prev_proxies
        logger.warning("keywords=%s. _get_vqd() is None, refreshing SESSION", keywords)
        VQD_CACHE.pop(keywords, None)
        sleep(0.25)

    # sleep to prevent blocking
    sleep(0.25)


def _refresh_vqd(keywords):
    VQD_CACHE.pop(keywords, None)
    vqd = _get_vqd(keywords)
    logger.debug("keywords=%s. _refresh_vqd()", keywords)
    return vqd


def _save_json(jsonfile, data):
    with open(jsonfile, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def _save_csv(csvfile, data):
    with open(csvfile, "w", newline="", encoding="utf-8") as file:
        if data:
            headers = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(data)


def _download_file(url, dir_path, filename):
    try:
        with requests.get(
            url, headers=HEADERS_FILE_DOWNLOAD, stream=True, timeout=10
        ) as resp:
            resp.raise_for_status()
            resp.raw.decode_content = True
            with open(os.path.join(dir_path, filename), "wb") as file:
                copyfileobj(resp.raw, file)
            logger.info(f"File downloaded {url}")
    except Exception:
        logger.exception("")


def _normalize(raw_html):
    """strip HTML tags"""
    if raw_html:
        return unescape(re.sub(RE_STRIP_TAGS, "", raw_html))


def _do_output(module_name, keywords, output, results):
    keywords = keywords.replace('"', "'")
    if output == "csv":
        _save_csv(
            f"{module_name}_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.csv", results
        )
    elif output == "json":
        _save_json(
            f"{module_name}_{keywords}_{datetime.now():%Y%m%d_%H%M%S}.json", results
        )
    """
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=4))
            input()
    """
