# coding: utf-8
import platform


JYTHON = platform.system() == 'Java'


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


try:  # pragma: no cover
    from javax.xml.parsers import DocumentBuilderFactory
    from java.io import ByteArrayInputStream
    from javax.xml.xpath import XPathFactory
except ImportError:
    DocumentBuilderFactory = None
    ByteArrayInputStream = None
    XPathFactory = None
