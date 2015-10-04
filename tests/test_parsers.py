# coding: utf-8
import re

import pytest

from ._compat import patch
from .conftest import ChildParser, SimpleParser, lxml_is_supported, lxml_is_not_supported
from pyanyapi import XMLObjectifyParser, XMLParser, JSONParser, YAMLParser, RegExpParser, AJAXParser, CSVParser
from pyanyapi.exceptions import ResponseParseError


HTML_CONTENT = "<html><body><a href='#test'></body></html>"
XML_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<id>32e9a4a2</id>
<test-mode>1</test-mode>
<type>accept</type>
</response>
'''
JSON_CONTENT = '{"container":{"test":"value"},"another":"123"}'
YAML_CONTENT = 'container:\n    test: "123"'
AJAX_CONTENT = '{"content": "<p>Pcontent</p><span>SPANcontent</span>",' \
               '"second_part":"<p>second_p</p>","third":{"inner":"<p>third_p</p>"}}'
MULTILINE_CONTENT = '123\n234'
CSV_CONTENT = '1,2,3\r\n4,5,6\r\n'
CSV_CONTENT_DIFFERENT_DELIMITER = '1;2;3\r\n4;5;6\r\n'


@lxml_is_supported
def test_xml_objectify_parser():
    parsed = XMLObjectifyParser().parse('<xml><test>123</test></xml>')
    assert parsed.test == 123
    assert parsed.not_existing is None


@lxml_is_supported
def test_xml_objectify_parser_error():
    parsed = XMLObjectifyParser().parse('<xml><test>123')
    with pytest.raises(ResponseParseError):
        parsed.test


@lxml_is_supported
def test_xml_parser_error():
    parsed = XMLParser({'test': None}).parse('<xml><test>123')
    with pytest.raises(ResponseParseError):
        parsed.test


def test_yaml_parser_error():
    parsed = YAMLParser({'test': 'test'}).parse('||')
    with pytest.raises(ResponseParseError):
        parsed.test


@lxml_is_supported
@pytest.mark.parametrize(
    'settings', (
        {'success': {'base': '//test-mode/text()'}},
        {'success': '//test-mode/text()'},
    )
)
def test_xml_parsed(settings):
    parsed = XMLParser(settings).parse(XML_CONTENT)
    assert parsed.success == ['1']
    assert parsed.parse('string(//id/text())') == '32e9a4a2'


@lxml_is_supported
def test_xml_simple_settings():
    assert XMLParser({'id': {'base': 'string(//id/text())'}}).parse(XML_CONTENT).id == '32e9a4a2'


def test_json_parsed():
    content = '''
    {
        "container":
        {
            "id": 1138003,
            "inner":
            [
                {
                    "end": {
                        "id": 123
                    }
                }
            ]
        }
    }
    '''

    parser = JSONParser({
        'success': {
            'base': 'container > inner > 0 > end > id'
        }
    })
    assert parser.parse(content).success == 123
    parser = JSONParser({
        'success': {
            'base': 'container > inner',
            'children': 'end > id',
        }
    })
    assert parser.parse(content).success == [123]


def test_multiple_parser_join():
    first_parser = RegExpParser({'test': 'href=\'(.*)\''})
    second_parser = JSONParser({'success': 'container > test'})
    for result_parser in ((first_parser & second_parser), (second_parser & first_parser)):
        assert result_parser.parse(HTML_CONTENT).test == '#test'
        assert result_parser.parse(JSON_CONTENT).success == 'value'
    third_parser = JSONParser({
        'fail': {
            'base': 'container > test',
        }
    })
    result_parser = first_parser & second_parser & third_parser
    assert result_parser.parse(JSON_CONTENT).success == 'value'


def test_multiply_parsers_declaration(dummy_parser):
    parsed = dummy_parser.parse(JSON_CONTENT)
    assert parsed.success == 'value'
    assert parsed.combined == '123-value'
    assert parsed.method('-123') == 'value-123'
    assert parsed.test is None

    parsed = dummy_parser.parse(HTML_CONTENT)
    assert parsed.test == '#test'
    assert parsed.success is None


@pytest.mark.parametrize(
    'content, attr, expected',
    (
        ('{"container":{"test":"value"}}', 'test', 'value'),
        ('{"container":{"test":"value"}}', 'second', None),
        ('{"container":{"fail":[1]}}', 'second', None),
        ('{"container":[[1],[],[3]]}', 'third', [1, None, 3]),
        ('{"container":null}', 'null', None),
        ('{"container":[1,2]}', 'test', '1,2'),
    )
)
def test_empty_values(empty_values_parser, content, attr, expected):
    parsed = empty_values_parser.parse(content)
    assert getattr(parsed, attr) == expected


def test_attributes(empty_values_parser):
    assert set(empty_values_parser.attributes) == set(['combined', 'test', 'test', 'second', 'null', 'third'])


def test_efficient_parsing(empty_values_parser):
    with patch.object(empty_values_parser.parsers[0], 'parse') as regexp_parser:
        assert empty_values_parser.parse(JSON_CONTENT).second is None
        assert not regexp_parser.called


@lxml_is_supported
def test_simple_config_xml_parser():
    parsed = XMLParser({'test': 'string(//test/text())'}).parse('<xml><test>123</test></xml>')
    assert parsed.test == '123'


def test_simple_config_json_parser():
    parsed = JSONParser({'test': 'container > test'}).parse(JSON_CONTENT)
    assert parsed.test == 'value'


def test_settings_inheritance():
    parser = ChildParser({'child2': 'override'})
    assert parser.settings['child2'] == 'override'
    assert parser.settings['child1'] == 'test3'
    assert parser.settings['parent2'] == 'child_override'
    assert parser.settings['parent1'] == 'test1'


@lxml_is_supported
def test_complex_config():
    parsed = XMLParser({'test': {'base': '//test', 'children': 'text()|*//text()'}}).parse(
        '<xml><test>123 </test><test><inside> 234</inside></test></xml>'
    )
    assert parsed.test == ['123 ', ' 234']


def test_json_parse():
    assert JSONParser({'test': 'container > test'}).parse(JSON_CONTENT).parse('another') == '123'


def test_json_value_error_parse():
    assert JSONParser({'test': 'container > test'}).parse('{"container":"1"}').test is None


def test_regexp_parse():
    assert RegExpParser({'digits': '\d+'}).parse('123abc').parse('[a-z]+') == 'abc'


def test_yaml_parse():
    assert YAMLParser({'test': 'container > test'}).parse(YAML_CONTENT).test == '123'


@lxml_is_not_supported
def test_lxml_not_supported():
    with pytest.raises(AssertionError):
        XMLParser({'test': '//p'}).parse('')


@lxml_is_supported
def test_ajax_parser():
    parsed = AJAXParser({'p': 'content > string(//p)', 'span': 'content > string(//span)'}).parse(AJAX_CONTENT)
    assert parsed.p == 'Pcontent'
    assert parsed.span == 'SPANcontent'
    assert parsed.parse('third > inner > string(//p)') == 'third_p'


@lxml_is_supported
def test_ajax_parser_cache():
    parsed = AJAXParser({
        'p': 'content > string(//p)',
        'span': 'content > string(//span)',
        'second': 'second_part > string(//p)'
    }).parse(AJAX_CONTENT)
    assert parsed.p == 'Pcontent'
    inner_interface = parsed._inner_cache['content']
    with patch.object(inner_interface, 'parse', wraps=inner_interface.parse) as patched:
        assert parsed.span == 'SPANcontent'
        assert len(parsed._inner_cache) == 1
        assert patched.call_count == 1
        assert parsed.second == 'second_p'
        assert patched.call_count == 1
        assert len(parsed._inner_cache) == 2


@lxml_is_supported
def test_ajax_parser_invalid_settings():
    parsed = AJAXParser({
        'valid': 'third > inner > string(//p)',
        'invalid': 'third > string(//p)',
    }).parse(AJAX_CONTENT)
    assert parsed.valid == 'third_p'
    assert parsed.invalid == ''


def test_parse_memoization():
    api = JSONParser().parse(JSON_CONTENT)
    with patch.object(api, 'get_from_dict', wraps=api.get_from_dict) as patched:
        assert api.parse('container > test') == 'value'
        assert patched.call_count == 1
        assert api.parse('container > test') == 'value'
        assert patched.call_count == 1


def test_regexp_settings():
    assert RegExpParser({'test': '\d+.\d+'}).parse(MULTILINE_CONTENT).test == '123'
    assert RegExpParser({'test': '\d+.\d+'}, flags=re.DOTALL).parse(MULTILINE_CONTENT).test == '123\n234'


def test_parse_all():
    expected = {'test': '123\n234', 'test2': '123', 'test3': None, 'test4': '123_4'}
    parser = SimpleParser(flags=re.DOTALL)
    assert parser.parse(MULTILINE_CONTENT).parse_all() == expected
    assert parser.parse_all(MULTILINE_CONTENT) == expected


def test_parse_all_combined_parser(dummy_parser):
    assert dummy_parser.parse(JSON_CONTENT).parse_all() == {
        'success': 'value',
        'combined': '123-value',
        'test': None
    }


def test_parse_csv():
    api = CSVParser({'second': '1:2'}).parse(CSV_CONTENT)
    assert api.second == '6'
    assert api.parse('0:1') == '2'
    assert api.parse('0:6') is None


def test_parse_csv_custom_delimiter():
    api = CSVParser({'second': '1:2'}, delimiter=';').parse(CSV_CONTENT_DIFFERENT_DELIMITER)
    assert api.second == '6'
    assert api.parse('0:1') == '2'
    assert api.parse('0:6') is None


def test_csv_parser_error():
    parsed = CSVParser({'test': '1:1'}).parse(123)
    with pytest.raises(ResponseParseError):
        parsed.test
