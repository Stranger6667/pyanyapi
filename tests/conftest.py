# coding: utf-8
import pytest

from pyanyapi import HTMLParser, JSONParser, RegExpParser, CombinedParser, interface_property, interface_method


class EmptyValuesParser(CombinedParser):
    parsers = [
        RegExpParser({'test': '\d,\d'}),
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

    @interface_method
    def method(self, value):
        return self.success + value


@pytest.fixture
def dummy_parser():
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
