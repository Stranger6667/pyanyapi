# coding: utf-8
"""
Module provides tools for convenient interface creation over various types of data in a declarative way.
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
    CSVParser,
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
    CSVInterface,
)
from .decorators import interface_property, interface_method
