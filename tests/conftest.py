# coding: utf-8
import platform
import sys

import pytest

from pyanyapi import JSONParser, RegExpParser, CombinedParser, interface_property, interface_method


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


class SimpleParser(RegExpParser):
    settings = {
        'test': '\d+.\d+',
        'test2': '\d+',
        'test3': 'a',
    }

    @interface_property
    def test4(self):
        return self.test2 + '_4'

    @interface_method
    def test_5(self, value):
        return 'Will not be included'


PYPY3 = hasattr(sys, 'pypy_translation_info') and sys.version_info[0] == 3
JYTHON = platform.system() == 'Java'

lxml_is_supported = pytest.mark.skipif(PYPY3 or JYTHON, reason='lxml is not supported')
lxml_is_not_supported = pytest.mark.skipif(not (PYPY3 or JYTHON), reason='Only on if lxml is supported')
