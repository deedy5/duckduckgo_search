import asyncio
import logging
from threading import Thread
from typing import Coroutine, Dict, List, Optional

from .duckduckgo_search_async import AsyncDDGS

logger = logging.getLogger("duckduckgo_search.DDGS")


class DDGS(AsyncDDGS):
    def __init__(self, headers=None, proxies=None, timeout=10, concurrency=5) -> None:
        super().__init__(headers, proxies, timeout, concurrency)
        self._loop = asyncio.new_event_loop()
        self._thread = Thread(target=self._loop.run_forever, daemon=True)  # run asyncio loop in a separate thread
        self._thread.start()

    def __enter__(self) -> "DDGS":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self):
        # close if DDGS is not used as context manager
        self.close()

    def close(self):
        if not self._thread.is_alive():
            return
        for task in asyncio.all_tasks(self._loop):
            task.cancel()
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()
        self._loop.close()

    def _run_async_in_thread(self, coro: Coroutine) -> Optional[List[Dict[str, Optional[str]]]]:
        """Runs an async coroutine in a separate thread."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def text(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().text(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def images(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().images(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def videos(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().videos(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def news(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().news(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def answers(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().answers(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def suggestions(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().suggestions(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def maps(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().maps(*args, **kwargs)
        return self._run_async_in_thread(async_coro)

    def translate(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        async_coro = super().translate(*args, **kwargs)
        return self._run_async_in_thread(async_coro)
