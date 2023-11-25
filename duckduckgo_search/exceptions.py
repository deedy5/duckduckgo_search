class DuckDuckGoSearchException(Exception):
    """Base exception class for duckduckgo_search."""


class APIException(DuckDuckGoSearchException):
    """Exception raised for API errors."""


class HTTPException(DuckDuckGoSearchException):
    """Exception raised for HTTP errors."""


class RateLimitException(DuckDuckGoSearchException):
    """Exception raised for rate limit errors."""


class TimeoutException(DuckDuckGoSearchException):
    """Exception raised for timeout errors."""


class VQDExtractionException(DuckDuckGoSearchException):
    """Exception raised for error in extract vqd."""
