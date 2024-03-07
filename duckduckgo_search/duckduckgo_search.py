import asyncio
from concurrent.futures import Future
from threading import Thread
from types import TracebackType
from typing import Any, Awaitable, Dict, Optional, Type, Union

from .duckduckgo_search_async import AsyncDDGS

# Create an event loop and run it in a separate thread.
_SHARED_LOOP: asyncio.AbstractEventLoop = asyncio.new_event_loop()
_SHARED_THREAD: Thread = Thread(target=_SHARED_LOOP.run_forever, daemon=True)
_SHARED_THREAD.start()


class DDGS(AsyncDDGS):
    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        proxies: Union[Dict[str, str], str, None] = None,
        timeout: Optional[int] = 10,
    ) -> None:
        super().__init__(headers=headers, proxies=proxies, timeout=timeout)
        self._loop = _SHARED_LOOP

    def __enter__(self) -> "DDGS":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        return True

    def _run_async_in_thread(self, coro: Awaitable[Any]) -> Any:
        """Runs an async coroutine in a separate thread."""
        future: Future[Any] = asyncio.run_coroutine_threadsafe(coro, self._loop)
        result = future.result()
        return result

    def text(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().text(*args, **kwargs))

    def images(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().images(*args, **kwargs))

    def videos(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().videos(*args, **kwargs))

    def news(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().news(*args, **kwargs))

    def answers(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().answers(*args, **kwargs))

    def suggestions(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().suggestions(*args, **kwargs))

    def maps(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().maps(*args, **kwargs))

    def translate(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async_in_thread(super().translate(*args, **kwargs))
