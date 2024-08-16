from __future__ import annotations

import asyncio
from types import TracebackType

from .duckduckgo_search import DDGS


class AsyncDDGS(DDGS):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxies: dict[str, str] | str | None = None,  # deprecated
        timeout: int | None = 10,
    ) -> None:
        """Initialize the AsyncDDGS object.

        Args:
            headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
            proxy (str, optional): proxy for the HTTP client, supports http/https/socks5 protocols.
                example: "http://user:pass@example.com:3128". Defaults to None.
            timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
        """
        super().__init__(headers=headers, proxy=proxy, proxies=proxies, timeout=timeout)
        self._loop = asyncio.get_running_loop()
        self._executor = super()._executor

    async def __aenter__(self) -> AsyncDDGS:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    async def achat(self, keywords: str, model: str = "gpt-4o-mini", timeout: int = 30) -> str:
        """Initiates async chat session with DuckDuckGo AI.

        Args:
            keywords (str): The initial message or question to send to the AI.
            model (str): The model to use: "gpt-4o-mini", "claude-3-haiku", "llama-3.1-70b", "mixtral-8x7b".
                Defaults to "gpt-4o-mini".
            timeout (int): Timeout value for the HTTP client. Defaults to 30.

        Returns:
            str: The response from the AI.
        """
        result = await self._loop.run_in_executor(self._executor, super().chat, keywords, model, timeout)
        return result

    async def atext(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        backend: str = "api",
        max_results: int | None = None,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async text search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            backend: api, html, lite. Defaults to api.
                api - collect data from https://duckduckgo.com,
                html - collect data from https://html.duckduckgo.com,
                lite - collect data from https://lite.duckduckgo.com.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with search results, or None if there was an error.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor, super().text, keywords, region, safesearch, timelimit, backend, max_results
        )
        return result

    async def aimages(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        size: str | None = None,
        color: str | None = None,
        type_image: str | None = None,
        layout: str | None = None,
        license_image: str | None = None,
        max_results: int | None = None,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async images search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: Day, Week, Month, Year. Defaults to None.
            size: Small, Medium, Large, Wallpaper. Defaults to None.
            color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
                Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
            type_image: photo, clipart, gif, transparent, line.
                Defaults to None.
            layout: Square, Tall, Wide. Defaults to None.
            license_image: any (All Creative Commons), Public (PublicDomain),
                Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
                Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
                Use Commercially). Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with images search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().images,
            keywords,
            region,
            safesearch,
            timelimit,
            size,
            color,
            type_image,
            layout,
            license_image,
            max_results,
        )
        return result

    async def avideos(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        resolution: str | None = None,
        duration: str | None = None,
        license_videos: str | None = None,
        max_results: int | None = None,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async videos search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            resolution: high, standart. Defaults to None.
            duration: short, medium, long. Defaults to None.
            license_videos: creativeCommon, youtube. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with videos search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().videos,
            keywords,
            region,
            safesearch,
            timelimit,
            resolution,
            duration,
            license_videos,
            max_results,
        )
        return result

    async def anews(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        max_results: int | None = None,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async news search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with news search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().news,
            keywords,
            region,
            safesearch,
            timelimit,
            max_results,
        )
        return result

    async def aanswers(
        self,
        keywords: str,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async instant answers. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query,

        Returns:
            List of dictionaries with instant answers results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().answers,
            keywords,
        )
        return result

    async def asuggestions(
        self,
        keywords: str,
        region: str = "wt-wt",
    ) -> list[dict[str, str]]:
        """DuckDuckGo async suggestions. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

        Returns:
            List of dictionaries with suggestions results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().suggestions,
            keywords,
            region,
        )
        return result

    async def amaps(
        self,
        keywords: str,
        place: str | None = None,
        street: str | None = None,
        city: str | None = None,
        county: str | None = None,
        state: str | None = None,
        country: str | None = None,
        postalcode: str | None = None,
        latitude: str | None = None,
        longitude: str | None = None,
        radius: int = 0,
        max_results: int | None = None,
    ) -> list[dict[str, str]]:
        """DuckDuckGo async maps search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query
            place: if set, the other parameters are not used. Defaults to None.
            street: house number/street. Defaults to None.
            city: city of search. Defaults to None.
            county: county of search. Defaults to None.
            state: state of search. Defaults to None.
            country: country of search. Defaults to None.
            postalcode: postalcode of search. Defaults to None.
            latitude: geographic coordinate (north-south position). Defaults to None.
            longitude: geographic coordinate (east-west position); if latitude and
                longitude are set, the other parameters are not used. Defaults to None.
            radius: expand the search square by the distance in kilometers. Defaults to 0.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with maps search results, or None if there was an error.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().maps,
            keywords,
            place,
            street,
            city,
            county,
            state,
            country,
            postalcode,
            latitude,
            longitude,
            radius,
            max_results,
        )
        return result

    async def atranslate(
        self,
        keywords: list[str] | str,
        from_: str | None = None,
        to: str = "en",
    ) -> list[dict[str, str]]:
        """DuckDuckGo async translate.

        Args:
            keywords: string or list of strings to translate.
            from_: translate from (defaults automatically). Defaults to None.
            to: what language to translate. Defaults to "en".

        Returns:
            List od dictionaries with translated keywords.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.
        """
        result = await self._loop.run_in_executor(
            self._executor,
            super().translate,
            keywords,
            from_,
            to,
        )
        return result
