# coding: utf-8
from .conftest import lxml_is_supported
from pyanyapi import RegExpParser, JSONParser, AJAXParser, XMLParser


JSON_CONTENT = '{"container":" 1 "}'
AJAX_CONTENT = '{"content": "<p> Pcontent </p>"}'
XML_CONTENT = '<p> Pcontent </p>'


def test_strip_regexp_parser():
    settings = {'all': '.+'}
    assert RegExpParser(settings).parse(' 1 ').all == ' 1 '
    assert RegExpParser(settings, strip=True).parse(' 1 ').all == '1'


def test_strip_json_parser():
    settings = {'all': 'container'}
    assert JSONParser(settings).parse(JSON_CONTENT).all == ' 1 '
    assert JSONParser(settings, strip=True).parse(JSON_CONTENT).all == '1'


@lxml_is_supported
def test_strip_ajax_parser():
    settings = {'all': 'content > string(//p)'}
    assert AJAXParser(settings).parse(AJAX_CONTENT).all == ' Pcontent '
    assert AJAXParser(settings, strip=True).parse(AJAX_CONTENT).all == 'Pcontent'


@lxml_is_supported
def test_strip_xml_parser():
    settings = {'all': 'string(//p)'}
    assert XMLParser(settings).parse(XML_CONTENT).all == ' Pcontent '
    assert XMLParser(settings, strip=True).parse(XML_CONTENT).all == 'Pcontent'
