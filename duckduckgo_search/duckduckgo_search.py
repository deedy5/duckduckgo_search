import asyncio
import logging
from typing import Dict, Generator, Optional

from .duckduckgo_search_async import AsyncDDGS

logger = logging.getLogger("duckduckgo_search.DDGS")


class DDGS(AsyncDDGS):
    def __init__(self, headers=None, proxies=None, timeout=10):
        super().__init__(headers, proxies, timeout)
        self._loop = asyncio.new_event_loop()

    def __enter__(self) -> "DDGS":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._loop.run_until_complete(self.__aexit__(exc_type, exc_val, exc_tb))

    def _iter_over_async(self, ait):
        """Iterate over an async generator."""
        ait = ait.__aiter__()
        get_next = ait.__anext__
        while True:
            try:
                obj = self._loop.run_until_complete(get_next())
                yield obj
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
        return self._loop.run_until_complete(async_coro)
