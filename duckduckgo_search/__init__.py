"""Duckduckgo_search.

Search for words, documents, images, videos, news, maps and text translation
using the DuckDuckGo.com search engine.
"""

import asyncio
import logging
import sys

from .duckduckgo_search import DDGS
from .duckduckgo_search_async import AsyncDDGS
from .version import __version__

__all__ = ["DDGS", "AsyncDDGS", "__version__", "cli"]


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# A do-nothing logging handler
# https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("duckduckgo_search").addHandler(logging.NullHandler())
