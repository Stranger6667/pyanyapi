# coding: utf-8
from .conftest import lxml_is_supported, not_pypy
from pyanyapi.parsers import RegExpParser, JSONParser, AJAXParser, XMLParser, XMLObjectifyParser


JSON_CONTENT = '{"container":" 1 "}'
AJAX_CONTENT = '{"content": "<p> Pcontent </p>"}'
XML_CONTENT = '<p> Pcontent </p>'
OBJECTIFY_CONTENT = '''<xml>
<Messages><Message> abc </Message></Messages>
<test> bcd </test>
<first><second><third> inside </third></second></first>
</xml>'''


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


class CustomParser(RegExpParser):
    settings = {'all': '.+'}
    strip = True


def test_class_override():
    assert CustomParser().parse(' 1 ').all == '1'
    assert CustomParser(strip=False).parse(' 1 ').all == ' 1 '


@lxml_is_supported
def test_objectify_strip_default():
    default = XMLObjectifyParser().parse(OBJECTIFY_CONTENT)
    assert default.Messages.Message == ' abc '
    assert default.test == ' bcd '
    assert default.first.second.third == ' inside '


@lxml_is_supported
@not_pypy
def test_objectify_strip():
    with_strip = XMLObjectifyParser(strip=True).parse(OBJECTIFY_CONTENT)
    assert with_strip.Messages.Message == 'abc'
    assert with_strip.test == 'bcd'
    assert with_strip.first.second.third == 'inside'
