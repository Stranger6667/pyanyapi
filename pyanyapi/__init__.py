# coding: utf-8
"""
Module provides tools for convenient interface creation over various types of data in declarative way.
"""
from .parsers import (
    BaseParser,
    CombinedParser,
    HTMLParser,
    XMLParser,
    XMLObjectifyParser,
    JSONParser,
    YAMLParser,
    AJAXParser,
    RegExpParser,
)
from .interfaces import (
    BaseInterface,
    CombinedInterface,
    XPathInterface,
    XMLInterface,
    XMLObjectifyInterface,
    DictInterface,
    JSONInterface,
    YAMLInterface,
    AJAXInterface,
    RegExpInterface,
)
from .decorators import interface_property, interface_method
