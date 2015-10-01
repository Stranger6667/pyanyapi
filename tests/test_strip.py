# coding: utf-8
from pyanyapi import RegExpParser, JSONParser


JSON_CONTENT = '{"container":" 1 "}'


def test_strip_regexp_parser():
    settings = {'all': '.+'}
    assert RegExpParser(settings).parse(' 1 ').all == ' 1 '
    assert RegExpParser(settings, strip=True).parse(' 1 ').all == '1'


def test_strip_json_parser():
    settings = {'all': 'container'}
    assert JSONParser(settings).parse(JSON_CONTENT).all == ' 1 '
    assert JSONParser(settings, strip=True).parse(JSON_CONTENT).all == '1'
