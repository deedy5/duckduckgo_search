import json
import logging
from datetime import datetime
from time import sleep

from requests import ConnectionError

from .utils import _save_csv, _save_json, get_vqd, session

logger = logging.getLogger(__name__)


def ddg_translate(
    keywords,
    from_=None,
    to="en",
    output=None,
):
    """DuckDuckGo translate

    Args:
        keywords: string or a list of strings to translate
        from_: what language to translate from (defaults automatically). Defaults to None.
        to: what language to translate. Defaults to "en".
        output: print, csv, json. Defaults to None.

    Returns:
        DuckDuckGo translate results.
    """

    if not keywords:
        return None

    # get vqd
    vqd = get_vqd("translate")
    if not vqd:
        return
    sleep(0.75)

    # translate
    params = {
        "vqd": vqd,
        "query": "translate",
        "from": from_,
        "to": to,
    }

    if isinstance(keywords, str):
        keywords = [keywords]

    results = []
    for data in keywords:
        try:
            resp = session.post(
                "https://duckduckgo.com/translation.js",
                params=params,
                data=data.encode("utf-8"),
            )
            logger.info(
                "%s %s %s", resp.status_code, resp.url, resp.elapsed.total_seconds()
            )
            result = resp.json()
            result["original"] = data
            results.append(result)
        except ConnectionError:
            logger.error("Connection Error.")
        except Exception:
            logger.exception("Exception.", exc_info=True)
        sleep(0.2)

    # output
    keywords = keywords[0].replace('"', "'")
    if output == "csv":
        _save_csv(
            f"ddg_translate_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            results,
        )
    elif output == "json":
        _save_json(
            f"ddg_translate_{keywords}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            results,
        )
    elif output == "print":
        for i, result in enumerate(results, start=1):
            print(f"{i}.", json.dumps(result, ensure_ascii=False, indent=2))
            input()
    return results
