# coding: utf-8


class ResponseParseError(Exception):
    """
    Raises when data can not be parsed with specified parser.
    """

    def __init__(self, message, content):
        self.message = message
        self.content = content
