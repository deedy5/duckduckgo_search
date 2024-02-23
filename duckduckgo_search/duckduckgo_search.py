import asyncio
import logging
import queue
from threading import Thread
from typing import Dict, Generator, Optional

from .duckduckgo_search_async import AsyncDDGS

logger = logging.getLogger("duckduckgo_search.DDGS")


class DDGS(AsyncDDGS):
    def __init__(self, headers=None, proxies=None, timeout=10):
        super().__init__(headers, proxies, timeout)
        self._queue = queue.Queue()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._thread = Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

    def __enter__(self) -> "DDGS":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        for task in asyncio.all_tasks(self._loop):
            task.cancel()
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()
        self._loop.close()

    def _iter_over_async(self, async_gen):
        """Runs an asynchronous generator in a separate thread and yields results from the queue."""
        future = asyncio.run_coroutine_threadsafe(self._async_generator_to_queue(async_gen), self._loop)
        future.result()
        while self._queue.qsize():
            yield self._queue.get()

    async def _async_generator_to_queue(self, async_gen):
        """Coroutine to convert an asynchronous generator to a queue."""
        try:
            async for item in async_gen:
                self._queue.put(item)
        except StopAsyncIteration:
            self._queue.put(None)

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

    def translate(self, *args, **kwargs) -> Generator[Dict[str, Optional[str]], None, None]:
        async_gen = super().translate(*args, **kwargs)
        return self._iter_over_async(async_gen)
