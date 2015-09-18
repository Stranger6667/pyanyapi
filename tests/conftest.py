# coding: utf-8
import pytest

from pyanyapi import HTMLParser, JSONParser, RegExpResponseParser, CombinedParser, interface_property


class EmptyValuesParser(CombinedParser):
    parsers = [
        RegExpResponseParser({'test': '\d,\d'}),
        JSONParser(
            {
                'test': {
                    'base': 'container > test',
                },
                'second': {
                    'base': 'container > fail > 1',
                },
                'third': {
                    'base': 'container',
                    'children': '0'
                },
                'null': {
                    'base': 'container',
                }
            }
        )
    ]

    @interface_property
    def combined(self):
        return '123-' + self.null


@pytest.fixture
def empty_values_parser():
    return EmptyValuesParser()


class DummyParser(CombinedParser):
    parsers = (
        JSONParser(
            {
                'success': {
                    'base': 'container > test',
                }
            }
        ),
        HTMLParser(
            {
                'test': {'base': 'string(//a/@href)'}
            }
        ),
    )

    @interface_property
    def combined(self):
        return '123-' + self.success


@pytest.fixture
def dummy_parser():
    return DummyParser()
