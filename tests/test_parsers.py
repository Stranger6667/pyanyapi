# coding: utf-8
from pyanyapi import XMLObjectifyParser


def test_xml_objectify_parser():
    parsed = XMLObjectifyParser().parse('<xml><test>123</test></xml>')
    assert parsed.test == 123
    assert parsed.not_existing is None
