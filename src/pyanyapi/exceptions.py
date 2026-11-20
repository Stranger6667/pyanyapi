from typing import Any


class ResponseParseError(Exception):
    """Raises when data can not be parsed with specified parser."""

    def __init__(self, message: str, content: Any = None) -> None:
        super().__init__(message)
        self.content = content
