"""Duckduckgo_search
~~~~~~~~~~~~~~
Search for words, documents, images, videos, news, maps and text translation
using the DuckDuckGo.com search engine.
"""

import logging

# ruff: noqa: F401
# isort: off
from .compat import (
    ddg,
    ddg_answers,
    ddg_images,
    ddg_maps,
    ddg_news,
    ddg_suggestions,
    ddg_translate,
    ddg_videos,
)

# isort: on
from .duckduckgo_search import DDGS
from .duckduckgo_search_async import AsyncDDGS
from .version import __version__

# A do-nothing logging handler
# https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("duckduckgo_search").addHandler(logging.NullHandler())
