class ResponseParseError(Exception):
    """Raises when data can not be parsed with specified parser."""

    def __init__(self, message, content=None):
        super().__init__(message)
        self.content = content
