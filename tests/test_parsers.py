# coding: utf-8
import pytest

from pyanyapi import XMLObjectifyParser
from pyanyapi.exceptions import ResponseParseError


def test_xml_objectify_parser():
    parsed = XMLObjectifyParser().parse('<xml><test>123</test></xml>')
    assert parsed.test == 123
    assert parsed.not_existing is None


def test_xml_objectify_parser_error():
    parsed = XMLObjectifyParser().parse('<xml><test>123')
    with pytest.raises(ResponseParseError):
        parsed.test
