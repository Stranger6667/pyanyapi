# coding: utf-8


try:
    from lxml import etree, objectify

    HTMLParser = etree.HTMLParser
    XMLParser = etree.XMLParser
except ImportError:
    etree = None
    objectify = None
    HTMLParser = None
    XMLParser = None

try:
    import ujson as json
except ImportError:
    import json


try:
    string_types = (str, unicode)
except NameError:
    string_types = (str, )
