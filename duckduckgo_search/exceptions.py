class DuckDuckGoSearchException(Exception):
    """Base exception class for duckduckgo_search."""


class VQDExtractionException(DuckDuckGoSearchException):
    """Exception raised for error in extract vqd."""
