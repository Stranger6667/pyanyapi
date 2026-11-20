# coding: utf-8
import pytest

from pyanyapi.decorators import interface_property, interface_method
from pyanyapi.parsers import JSONParser, RegExpParser, CombinedParser, HTMLParser


class EmptyValuesParser(CombinedParser):
    parsers = [
        RegExpParser({'test': r'\d,\d'}),
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


@pytest.fixture
def dummy_parser():

    class DummyParser(CombinedParser):
        parsers = (
            JSONParser({'success': 'container > test'}),
            RegExpParser({'test': 'href=\'(.*)\''}),
        )

        @interface_property
        def combined(self):
            return '123-' + self.success

        @interface_method
        def method(self, value):
            return self.success + value

    return DummyParser()


class ParentParser(JSONParser):
    settings = {
        'parent1': 'test1',
        'parent2': 'test2'
    }


class ChildParser(ParentParser):
    settings = {
        'parent2': 'child_override',
        'child1': 'test3',
        'child2': 'test4'
    }


class SubParser(HTMLParser):
    settings = {
        'href': 'string(//@href)',
        'text': 'string(//text())'
    }


class SimpleParser(RegExpParser):
    settings = {
        'test': r'\d+.\d+',
        'test2': r'\d+',
        'test3': 'a',
    }

    @interface_property
    def test4(self):
        return self.test2 + '_4'

    @interface_method
    def test_5(self, value):
        return 'Will not be included'

