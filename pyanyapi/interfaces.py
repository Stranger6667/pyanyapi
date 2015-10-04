# coding: utf-8
"""
Classes to be filled with interface declarations.
"""
import csv
import re

import yaml

from ._compat import json, etree, objectify, XMLParser, HTMLParser, string_types
from .exceptions import ResponseParseError
from .helpers import memoize


DICT_LOOKUP = ' > '


class BaseInterface(object):
    """
    Basic dynamically generated interface.
    """
    content = None
    empty_result = None

    def __init__(self, content, strip=False):
        self.content = content
        self.strip = strip
        self.parse = memoize(self.parse)

    @classmethod
    def init_attr(cls, settings):

        def inner(self):
            return cls.execute_method(self, settings)

        return inner

    def execute_method(self, settings):
        raise NotImplementedError

    @property
    def parsed_content(self):
        if not hasattr(self, '_parsed_content'):
            self._parsed_content = self.perform_parsing()
        return self._parsed_content

    def perform_parsing(self):
        raise NotImplementedError

    def parse(self, query):
        raise NotImplementedError

    def parse_all(self):
        """
        Processes all available properties and returns results as dictionary.
        """
        return dict(
            (key, getattr(self, key, self.empty_result))
            for key, attr in self.__class__.__dict__.items()
            if hasattr(attr, '_attached') and type(attr).__name__ == 'cached_property'
        )

    def maybe_strip(self, value):
        if self.strip and isinstance(value, string_types):
            return value.strip()
        return value


# Uses as fallback. None - can be obtained from JSON's null, any string also can be, so unique object is a best choice
EMPTY_RESULT = object()


class CombinedInterface(BaseInterface):

    def __init__(self, parsers, *args, **kwargs):
        self.parsers = parsers
        super(CombinedInterface, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        # Catch self.parsers and dynamically attached attributes
        try:
            return super(CombinedInterface, self).__getattribute__(item)
        except AttributeError:
            return self.walk(item)

    def walk(self, item):
        """
        Recursively walks through all available parsers.
        """
        for parser in self.parsers:
            try:
                if item not in parser.attributes:
                    continue
                result = getattr(parser.parse(self.content), item, EMPTY_RESULT)
                # Ignore empty results in current parser
                if result in (EMPTY_RESULT, parser.interface_class.empty_result):
                    continue
                return result
            except (AttributeError, ResponseParseError):
                pass

    def parse_all(self):
        result = super(CombinedInterface, self).parse_all()
        for parser in self.parsers:
            result.update(parser.parse_all(self.content))
        return result


class XPathInterface(BaseInterface):
    """
    Uses as base class for HTML/XML-based content.
    Use XPath 1.0 syntax, which is compatible with LXML.
    Because of lack of support of XPath 2.0 some parts of settings structure
    is not intuitive.
    Settings example:

    {
        'errors': {
            'base': "//ul[@class='alerts']/div",
            'children': 'text()|*//text()'
        }
    }

    'children' key usually uses for modification of result of 'base' expression
    before concatenation.
    """
    parser_class = HTMLParser
    empty_result = ''
    _error_message = 'HTML data can not be parsed.'

    def perform_parsing(self):
        try:
            return etree.fromstring(self.content, self.parser_class())
        except etree.XMLSyntaxError:
            raise ResponseParseError(self._error_message)

    def execute_method(self, settings):
        if isinstance(settings, dict):
            result = self.parse(settings['base'])
            child_query = settings.get('children')
            if child_query:
                return [self.maybe_strip(''.join(element.xpath(child_query))) for element in result]
            return result

        return self.parse(settings)

    def parse(self, query):
        return self.maybe_strip(self.parsed_content.xpath(query))


class XMLInterface(XPathInterface):
    parser_class = XMLParser
    _error_message = 'XML data can not be parsed.'


class XMLObjectifyInterface(BaseInterface):
    """
    Parse XML in the way, that its attributes can be accessed like attributes of python object:

    <xml><test>123</test></xml>

    From it you can get:
    >> obj.test
    123
    >> obj.not_test
    None

    Also this interface does not require any settings.
    """
    _error_message = 'XML data can not be parsed.'

    def perform_parsing(self):
        try:
            return objectify.fromstring(self.content)
        except etree.XMLSyntaxError:
            raise ResponseParseError(self._error_message)

    def __getattribute__(self, item):
        try:
            return super(XMLObjectifyInterface, self).__getattribute__(item)
        except AttributeError:
            if item == '_parsed_content':
                raise
            try:
                return self.parsed_content.__getattribute__(item)
            except AttributeError:
                return None


class DictInterface(BaseInterface):
    """
    Interface for python dictionaries. Based on PostgreSQL statements syntax.

    {
        'external_id': 'container > id'
    }

    which will get "123" from {"container":{"id":"123"}}
    """

    def get_from_dict(self, target, query):
        if not target:
            return target
        action_list = query.split(DICT_LOOKUP)
        for action in action_list:
            if target:
                action = action.strip()
                if isinstance(target, dict):
                    target = target.get(action, self.empty_result)
                else:
                    try:
                        target = target[int(action)]
                    except (IndexError, TypeError, ValueError):
                        return self.empty_result
            else:
                return target
        return self.maybe_strip(target)

    def execute_method(self, settings):
        if isinstance(settings, dict):
            result = self.parse(settings['base'])
            child_query = settings.get('children')
            if child_query:
                return [
                    self.get_from_dict(r, child_query) or self.empty_result for r in result
                ] if result else self.empty_result
            return result

        return self.parse(settings)

    def parse(self, query):
        return self.get_from_dict(self.parsed_content, query)


class JSONInterface(DictInterface):
    _error_message = 'JSON data can not be parsed.'

    def perform_parsing(self):
        try:
            return json.loads(self.content)
        except (ValueError, TypeError):
            raise ResponseParseError(self._error_message)


class YAMLInterface(DictInterface):
    _error_message = 'YAML data can not be parsed.'

    def perform_parsing(self):
        try:
            return yaml.load(self.content)
        except yaml.error.YAMLError:
            raise ResponseParseError(self._error_message)


class AJAXInterface(JSONInterface):
    """
    Allows to execute XPath, combined with dictionary-based lookups from DictInterface.

    {
        'p': 'container > string(//p)'
    }

    which will get "p_content" from {"container":"<p>p_content</p>"}
    """
    inner_interface_class = XPathInterface

    def __init__(self, *args, **kwargs):
        self._inner_cache = {}
        super(AJAXInterface, self).__init__(*args, **kwargs)

    def get_inner_interface(self, text, json_part):
        if json_part not in self._inner_cache:
            inner_content = super(AJAXInterface, self).get_from_dict(text, json_part)
            self._inner_cache[json_part] = self.inner_interface_class(inner_content, self.strip)
        return self._inner_cache[json_part]

    def get_from_dict(self, target, query):
        json_part, xpath_part = query.rsplit(DICT_LOOKUP, 1)
        inner_interface = self.get_inner_interface(target, json_part)
        try:
            return inner_interface.parse(xpath_part)
        except (etree.XMLSyntaxError, ValueError):
            return inner_interface.empty_result


class RegExpInterface(BaseInterface):
    """
    Parser based on regular expressions. It is most powerful parser, because of
    its simplicity.
    Settings example:

    {
        "result": "^ok$",
        "errors": "^Error \d+$",
    }

    So, response will be like 'ok' or 'Error 100'.
    """

    def __init__(self, content, strip=False, flags=0):
        self.flags = flags
        super(RegExpInterface, self).__init__(content, strip)

    def execute_method(self, settings):
        matches = re.findall(settings, self.content, self.flags)
        if matches:
            return self.maybe_strip(matches[0])
        return self.empty_result

    def parse(self, query):
        return self.execute_method(query)


class CSVInterface(BaseInterface):
    """
    Operates with CSV data with simple queries in format 'row_id:column_id'.

    {
        "value": "1:2"
    }

    Will get 6 from "1,2,3\r\n4,5,6"
    """
    _error_message = 'CSV data can not be parsed.'

    def __init__(self, content, strip=False, **reader_kwargs):
        self.reader_kwargs = reader_kwargs
        super(CSVInterface, self).__init__(content, strip)

    def perform_parsing(self):
        try:
            return list(csv.reader(self.content.split(), **self.reader_kwargs))
        except (TypeError, AttributeError):
            raise ResponseParseError(self._error_message)

    def execute_method(self, settings):
        row, column = settings.split(':')
        try:
            return self.parsed_content[int(row)][int(column)]
        except (IndexError, TypeError):
            return self.empty_result

    def parse(self, query):
        return self.execute_method(query)
