# coding: utf-8
"""
Module provides tools to creates convenient interfaces over
various types of data in declarative way.
"""
from .parsers import (
    ResponseParser,
    CombinedParser,
    HTMLParser,
    XMLParser,
    XMLObjectifyParser,
    JSONParser,
    RegExpResponseParser,
    SOAPParser,
)
from .interfaces import (
    BaseInterface,
    XPathInterface,
    XMLInterface,
    JSONInterface,
    RegExpInterface,
    SOAPInterface,
)
from .decorators import interface_property, interface_method
