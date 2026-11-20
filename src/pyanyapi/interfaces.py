"""Classes to be filled with interface declarations."""

import csv
import json
import re
from collections.abc import Callable, Sequence
from functools import cache
from typing import TYPE_CHECKING, Any

import yaml
from lxml import etree, objectify
from lxml.etree import HTMLParser, XMLParser

from .exceptions import ResponseParseError

if TYPE_CHECKING:
    from .parsers import BaseParser

DICT_LOOKUP = " > "


def expand_results(value: Any) -> Any:
    if isinstance(value, list):
        return [item.parse_all() for item in value]
    return value


class BaseInterface:
    """Basic dynamically generated interface."""

    content: Any = None
    empty_result: Any = None
    _parsed_content: Any

    def __init__(self, content: Any, strip: bool = False) -> None:
        self.content = content
        self.strip = strip
        self.parse = cache(self.parse)  # type: ignore[method-assign]

    if TYPE_CHECKING:
        # Attributes are generated from parser settings at runtime
        def __getattr__(self, name: str) -> Any: ...

    @classmethod
    def init_attr(cls, settings: Any) -> Callable[["BaseInterface"], Any]:

        def inner(self: BaseInterface) -> Any:
            return cls.execute_method(self, settings)

        return inner

    def execute_method(self, settings: Any) -> Any:
        raise NotImplementedError

    @property
    def parsed_content(self) -> Any:
        if not hasattr(self, "_parsed_content"):
            self._parsed_content = self.perform_parsing()
        return self._parsed_content

    def perform_parsing(self) -> Any:
        raise NotImplementedError

    def parse(self, query: Any) -> Any:
        raise NotImplementedError

    def parse_all(self) -> dict[str, Any]:
        """Processes all available properties and returns results as dictionary."""
        return {
            key: expand_results(getattr(self, key, self.empty_result))
            for key, attr in self.__class__.__dict__.items()
            if hasattr(attr, "_attached") and type(attr).__name__ == "cached_property"
        }

    def maybe_strip(self, value: Any) -> Any:
        if self.strip and isinstance(value, str):
            return value.strip()
        return value


# Uses as fallback. None - can be obtained from JSON's null, any string also can be, so unique object is a best choice
EMPTY_RESULT = object()


class CombinedInterface(BaseInterface):
    def __init__(self, parsers: Sequence["BaseParser"], content: Any, strip: bool = False) -> None:
        self.parsers = parsers
        super().__init__(content, strip)

    def __getattribute__(self, item: str) -> Any:
        # Catch self.parsers and dynamically attached attributes
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.walk(item)

    def walk(self, item: str) -> Any:
        """Recursively walks through all available parsers."""
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
        return None

    def parse_all(self) -> dict[str, Any]:
        result = super().parse_all()
        for parser in self.parsers:
            result.update(parser.parse_all(self.content))
        return result


class XPathInterface(BaseInterface):
    """Uses as base class for HTML/XML-based content.

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

    parser_class: type[HTMLParser] | type[XMLParser] = HTMLParser
    empty_result = ""
    _error_message = "HTML data can not be parsed."

    def perform_parsing(self) -> Any:
        try:
            return etree.fromstring(self.content, self.parser_class())
        except etree.XMLSyntaxError as exc:
            raise ResponseParseError(self._error_message, self.content) from exc

    def execute_method(self, settings: Any) -> Any:
        if isinstance(settings, dict):
            result = self.parse(settings["base"])
            child_query = settings.get("children")
            if child_query:
                return [self.maybe_strip("".join(element.xpath(child_query))) for element in result]
            sub_parser = settings.get("parser")
            if sub_parser:
                return [
                    (sub_parser() if callable(sub_parser) else sub_parser).parse(etree.tostring(element))
                    for element in result
                ]
            return result

        return self.parse(settings)

    def parse(self, query: Any) -> Any:
        return self.maybe_strip(self.parsed_content.xpath(query))


class XMLInterface(XPathInterface):
    parser_class = XMLParser
    _error_message = "XML data can not be parsed."


class XMLObjectifyInterface(BaseInterface):
    """Parse XML in the way, that its attributes can be accessed like attributes of python object.

    <xml><test>123</test></xml>

    From it you can get:
    >> obj.test
    123
    >> obj.not_test
    None

    Also this interface does not require any settings.
    """

    _error_message = "XML data can not be parsed."

    def perform_parsing(self) -> Any:
        try:
            return objectify.fromstring(self.content)
        except etree.XMLSyntaxError as exc:
            raise ResponseParseError(self._error_message, self.content) from exc

    def __getattribute__(self, item: str) -> Any:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            if item == "_parsed_content":
                raise
            try:
                return self.maybe_strip(self.parsed_content.__getattribute__(item))
            except AttributeError:
                return None

    def maybe_strip(self, value: Any) -> Any:
        if self.strip and isinstance(value, objectify.ObjectifiedElement):
            if isinstance(value, objectify.StringElement):
                return value.text.strip() if value.text is not None else value
            # Not `value.__dict__`: on PyPy it is not lxml's children mapping, so nothing was stripped
            for child in value.iterdescendants(tag=etree.Element):
                if isinstance(child, objectify.StringElement) and child.text is not None:
                    child._setText(child.text.strip())
        return value


class DictInterface(BaseInterface):
    """Interface for python dictionaries. Based on PostgreSQL statements syntax.

    {
        'external_id': 'container > id'
    }

    which will get "123" from {"container":{"id":"123"}}
    """

    def get_from_dict(self, target: Any, query: str) -> Any:
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

    def execute_method(self, settings: Any) -> Any:
        if isinstance(settings, dict):
            result = self.parse(settings["base"])
            child_query = settings.get("children")
            if child_query:
                return (
                    [self.get_from_dict(r, child_query) or self.empty_result for r in result]
                    if result
                    else self.empty_result
                )
            return result

        return self.parse(settings)

    def parse(self, query: Any) -> Any:
        return self.get_from_dict(self.parsed_content, query)


class JSONInterface(DictInterface):
    _error_message = "JSON data can not be parsed."

    def perform_parsing(self) -> Any:
        try:
            return json.loads(self.content)
        except (ValueError, TypeError) as exc:
            raise ResponseParseError(self._error_message, self.content) from exc


class YAMLInterface(DictInterface):
    _error_message = "YAML data can not be parsed."

    def perform_parsing(self) -> Any:
        try:
            return yaml.safe_load(self.content)
        except yaml.error.YAMLError as exc:
            raise ResponseParseError(self._error_message, self.content) from exc


class AJAXInterface(JSONInterface):
    """Allows to execute XPath, combined with dictionary-based lookups from DictInterface.

    {
        'p': 'container > string(//p)'
    }

    which will get "p_content" from {"container":"<p>p_content</p>"}
    """

    inner_interface_class = XPathInterface

    def __init__(self, content: Any, strip: bool = False) -> None:
        self._inner_cache: dict[str, XPathInterface] = {}
        super().__init__(content, strip)

    def get_inner_interface(self, text: Any, json_part: str) -> "XPathInterface":
        if json_part not in self._inner_cache:
            inner_content = super().get_from_dict(text, json_part)
            self._inner_cache[json_part] = self.inner_interface_class(inner_content, self.strip)
        return self._inner_cache[json_part]

    def get_from_dict(self, target: Any, query: str) -> Any:
        json_part, xpath_part = query.rsplit(DICT_LOOKUP, 1)
        inner_interface = self.get_inner_interface(target, json_part)
        try:
            return inner_interface.parse(xpath_part)
        except (etree.XMLSyntaxError, ValueError, TypeError):
            return inner_interface.empty_result


class RegExpInterface(BaseInterface):
    r"""Parser based on regular expressions.

    It is the most powerful parser, because of its simplicity.
    Settings example:

    {
        "result": "^ok$",
        "errors": "^Error \d+$",
    }

    So, response will be like 'ok' or 'Error 100'.
    """

    def __init__(self, content: Any, strip: bool = False, flags: int = 0) -> None:
        self.flags = flags
        super().__init__(content, strip)

    def execute_method(self, settings: Any) -> Any:
        matches = re.findall(settings, self.content, self.flags)
        if matches:
            return self.maybe_strip(matches[0])
        return self.empty_result

    def parse(self, query: Any) -> Any:
        return self.execute_method(query)


class CSVInterface(BaseInterface):
    r"""Operates with CSV data with simple queries in format 'row_id:column_id'.

    {
        "value": "1:2"
    }

    Will get 6 from "1,2,3\r\n4,5,6"
    """

    _error_message = "CSV data can not be parsed."

    def __init__(self, content: Any, strip: bool = False, **reader_kwargs: Any) -> None:
        self.reader_kwargs = reader_kwargs
        super().__init__(content, strip)

    def perform_parsing(self) -> Any:
        try:
            return list(csv.reader(self.content.split(), **self.reader_kwargs))
        except (TypeError, AttributeError) as exc:
            raise ResponseParseError(self._error_message, self.content) from exc

    def execute_method(self, settings: Any) -> Any:
        row, column = settings.split(":")
        try:
            return self.parsed_content[int(row)][int(column)]
        except (IndexError, TypeError):
            return self.empty_result

    def parse(self, query: Any) -> Any:
        return self.execute_method(query)


class IndexOfInterface(BaseInterface):
    """Simple interface that tries to find specified string inside another string, storing boolean values.

    Settings example:
    {
        "has_bar": "bar",
        "has_foo": "foo"
    }
    If content contains "bar" string, interface property "has_bar" will be True.
    """

    _error_message = "Can not perform string search."

    def execute_method(self, settings: Any) -> Any:
        try:
            return str(settings) in str(self.content)
        except (TypeError, ValueError) as exc:
            raise ResponseParseError(self._error_message, self.content) from exc

    def parse(self, query: Any) -> Any:
        return self.execute_method(query)
