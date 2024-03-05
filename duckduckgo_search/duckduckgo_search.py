import asyncio
from threading import Thread
from typing import Coroutine, Dict, List, Optional

from .duckduckgo_search_async import AsyncDDGS

# Create an event loop and run it in a separate thread.
_SHARED_LOOP = asyncio.new_event_loop()
_SHARED_THREAD = Thread(target=_SHARED_LOOP.run_forever, daemon=True)
_SHARED_THREAD.start()


class DDGS(AsyncDDGS):
    def __init__(self, headers=None, proxies=None, timeout=10) -> None:
        super().__init__(headers, proxies, timeout)
        self._loop = _SHARED_LOOP

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _run_async_in_thread(self, coro: Coroutine) -> Optional[List[Dict[str, Optional[str]]]]:
        """Runs an async coroutine in a separate thread."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def text(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().text(*args, **kwargs))

    def images(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().images(*args, **kwargs))

    def videos(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().videos(*args, **kwargs))

    def news(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().news(*args, **kwargs))

    def answers(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().answers(*args, **kwargs))

    def suggestions(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().suggestions(*args, **kwargs))

    def maps(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().maps(*args, **kwargs))

    def translate(self, *args, **kwargs) -> Optional[List[Dict[str, Optional[str]]]]:
        return self._run_async_in_thread(super().translate(*args, **kwargs))
