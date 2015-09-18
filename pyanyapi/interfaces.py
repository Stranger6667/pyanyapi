# coding: utf-8
"""
Classes to be filled with interface declarations.
"""
import json
import re

from lxml import etree, objectify

from .exceptions import ResponseParseError


class BaseInterface(object):
    """
    Basic dynamically generated interface.
    """
    content = None
    empty_result = None

    def __init__(self, content):
        self.content = content

    @classmethod
    def init_attr(cls, settings):
        raise NotImplementedError

    @property
    def parsed_content(self):
        if not hasattr(self, '_parsed_content'):
            self._parsed_content = self.perform_parsing()
        return self._parsed_content

    def perform_parsing(self):
        return self.content


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
    parser_class = etree.HTMLParser
    empty_result = ''

    def perform_parsing(self):
        try:
            return etree.fromstring(self.content, self.parser_class())
        except etree.XMLSyntaxError:
            raise ResponseParseError('XML response can not be parsed.')

    @classmethod
    def init_attr(cls, settings):

        def inner(self):
            result = self.parsed_content.xpath(settings['base'])
            if settings.get('children'):
                return [''.join(element.xpath(settings['children'])).strip() for element in result]
            elif isinstance(result, list):
                return result
            else:
                return result.strip()

        return inner

    def parse(self, xpath):
        return self.parsed_content.xpath(xpath)


class XMLInterface(XPathInterface):
    parser_class = etree.XMLParser


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

    def perform_parsing(self):
        try:
            return objectify.fromstring(str(self.content))
        except etree.XMLSyntaxError:
            raise ResponseParseError('XML response can not be parsed.')

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


class JSONInterface(BaseInterface):
    """
    Interface for JSON. Based on PostgreSQL statements syntax.
    Settings example:

    {
        'external_id': {'base': 'container > id'}
    }

    which will get "123" from {"container":{"id":"123"}}
    """

    def perform_parsing(self):
        try:
            return json.loads(self.content)
        except (ValueError, TypeError):
            raise ResponseParseError('JSON response can not be parsed.')

    @classmethod
    def get_from_json(cls, text, data):
        action_list = data.split('>')
        result = text
        for action in action_list:
            action = action.strip()
            if result:
                if isinstance(result, dict):
                    result = result.get(action, cls.empty_result)
                else:
                    try:
                        result = result[int(action)]
                    except (IndexError, TypeError):
                        return cls.empty_result
        return result

    @classmethod
    def init_attr(cls, settings):

        def inner(self):
            result = self.get_from_json(self.parsed_content, settings['base'])

            if settings.get('children'):
                children = settings.get('children')
                return [
                    self.get_from_json(r, children) or cls.empty_result for r in result
                ] if result else cls.empty_result
            return result

        return inner


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

    def get_match(self, expression):
        expression = re.compile(expression)
        matches = expression.findall(self.content)
        if matches:
            return matches[0]
        return self.empty_result

    @classmethod
    def init_attr(cls, expression):

        def inner(self):
            return self.get_match(expression)

        return inner


class SOAPInterface(RegExpInterface):
    """
    Hack to be able to easy parse suds responses.
    """
    expression_template = r'<(ns1:)?{0}>(.*)</(ns1:)?{0}>'

    def get_match(self, attr_name):
        try:
            return re.findall(self.expression_template.format(attr_name), self.content, re.DOTALL)[0][1]
        except IndexError:
            return self.empty_result
