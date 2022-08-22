import csv
import json
import logging
import os
import re
import unicodedata

import requests
from lxml import html
from requests import ConnectionError, Timeout

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Referer": "https://duckduckgo.com/",
}
session.headers.update(headers)

logger = logging.getLogger(__name__)


def get_vqd(keywords):
    payload = {"q": keywords}
    try:
        resp = session.post(
            "https://duckduckgo.com", data=payload, headers=headers, timeout=10
        )
        if resp.status_code == 200:
            logger.info(
                "get_vqd(). response=200 in %s s.", resp.elapsed.total_seconds()
            )
            tree = html.fromstring(resp.content)
            vqd = (
                tree.xpath("//script[contains(text(), 'vqd=')]/text()")[0]
                .split("vqd='")[-1]
                .split("';")[0]
            )
            logger.info("keywords=%s. Got vqd=%s", keywords, vqd)
            return vqd
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    }
    for _ in range(3):
        try:
            resp = requests.get(image_url, headers=headers, timeout=20)
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


def _slugify(filename):
    """
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Strip leading and trailing whitespace, dashes, and underscores.
    """

    filename = unicodedata.normalize("NFC", filename)
    filename = re.sub(r"[^\w\s-]", "", filename.lower())
    return re.sub(r"[-\s]+", "-", filename).strip("-_")


def _normalize(text):
    if text:
        body = html.fromstring(text)
        return html.tostring(body, method="text", encoding="unicode")
