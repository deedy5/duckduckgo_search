import asyncio
import logging
from typing import Dict, Generator, Optional

import nest_asyncio

from .duckduckgo_search_async import AsyncDDGS

logger = logging.getLogger("duckduckgo_search.DDGS")
nest_asyncio.apply()


class DDGS(AsyncDDGS):
    def __init__(self, headers=None, proxies=None, timeout=10):
        super().__init__(headers, proxies, timeout)

    def __enter__(self) -> "DDGS":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        asyncio.run(super().__aexit__(exc_type, exc_val, exc_tb))

    def _iter_over_async(self, async_gen):
        """Iterate over an async generator."""
        while True:
            try:
                yield asyncio.run(async_gen.__anext__())
            except StopAsyncIteration:
                break

    def text(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().text(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def images(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().images(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def videos(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().videos(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def news(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().news(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def answers(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().answers(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def suggestions(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().suggestions(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def maps(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().maps(*args, **kwargs)
        return self._iter_over_async(async_gen)

    def translate(self, *args, **kwargs) -> Optional[Dict[str, Optional[str]]]:
        async_coro = super().translate(*args, **kwargs)
        return asyncio.run(async_coro)
