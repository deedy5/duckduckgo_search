import csv
import json
import logging
import os
import re
from datetime import datetime
from functools import lru_cache

import requests
from requests import ConnectionError, Timeout

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Referer": "https://duckduckgo.com/",
}
session.headers.update(headers)

logger = logging.getLogger(__name__)

RE_CLEAN_HTML = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
RE_VQD = re.compile(r"vqd=([0-9-]+)\&")


@lru_cache(maxsize=128)
def _get_vqd(keywords):
    payload = {"q": keywords}
    try:
        resp = session.post(
            "https://duckduckgo.com", data=payload, headers=headers, timeout=10
        )
        if resp.status_code == 200:
            logger.info(
                "%s %s %s", resp.status_code, resp.url, resp.elapsed.total_seconds()
            )
            vqd = RE_VQD.search(resp.text)
            logger.info("keywords=%s. Got vqd=%s", keywords, vqd)
            return vqd.group(1) if vqd else None
        logger.info("get_vqd(). response=%s", resp.status_code)
    except Timeout:
        logger.warning("Connection timeout in get_vqd().")
    except ConnectionError:
        logger.warning("Connection error in get_vqd().")
    except Exception:
        logger.exception("Exception in get_vqd().", exc_info=True)


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


def _download_image(image_url, dir_path, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    for _ in range(2):
        try:
            resp = requests.get(image_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                with open(os.path.join(dir_path, filename), "wb") as file:
                    file.write(resp.content)
                    logger.info("Image downloaded. image_url=%s", image_url)
                break
        except Timeout:
            logger.warning("Connection timeout. image_url=%s", image_url)
        except ConnectionError:
            logger.warning("Connection error. image_url=%s", image_url)
        except Exception:
            logger.warning("Exception. {image_url=}.", exc_info=True)


def _normalize(raw_html):
    if raw_html:
        return re.sub(RE_CLEAN_HTML, "", raw_html)


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
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=4))
            input()
