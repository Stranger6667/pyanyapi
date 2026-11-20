# Parsers

## HTML and XML

HTML and XML settings use XPath 1.0; lxml does not support XPath 2.0.
`XMLParser` works like `HTMLParser`, but uses a different lxml parser internally.
With `requests`:

```python
import requests

from pyanyapi.parsers import HTMLParser

parser = HTMLParser({"header": "string(.//h1/text())"})
response = requests.get("https://example.com")
api = parser.parse(response.text)
api.header  # "Example Domain"
```

Run more XPath queries at any time:

```python
from pyanyapi.parsers import HTMLParser

parser = HTMLParser({"header": "string(.//h1/text())"})
api = parser.parse("<html><body><h1>This is</h1><p>test</p></body></html>")
assert api.header == "This is"
assert api.parse("string(//p)") == "test"
```

## XML Objectify

lxml can convert a whole XML document into a Python object.
This parser does not need any settings:

```python
from pyanyapi.parsers import XMLObjectifyParser

assert XMLObjectifyParser().parse("<xml><test>123</test></xml>").test == 123
```

## JSON

The settings syntax is based on PostgreSQL JSON operators:

```python
from pyanyapi.parsers import JSONParser

assert JSONParser({"id": "container > id"}).parse('{"container": {"id": "123"}}').id == "123"
```

Access list items by index:

```python
from pyanyapi.parsers import JSONParser

api = JSONParser({"second": "container > 1"}).parse('{"container": ["first", "second", "third"]}')
assert api.second == "second"
```

Run more queries after the initial parsing:

```python
from pyanyapi.parsers import JSONParser

api = JSONParser({"second": "container > 1"}).parse('{"container": [], "second_container": [123]}')
assert api.parse("second_container > 0") == 123
```

## YAML

Works like the JSON parser, but with YAML data:

```python
from pyanyapi.parsers import YAMLParser

assert YAMLParser({"test": "container > test"}).parse('container:\n    test: "123"').test == "123"
```

## Regular expressions

When data has a broken format or is too complicated for the other parsers, use regular expressions:

```python
from pyanyapi.parsers import RegExpParser

api = RegExpParser({"error_code": r"Error (\d+)"}).parse("Oh no!!! It is Error 100!!!")
assert api.error_code == "100"
```

Run more queries after the initial parsing:

```python
from pyanyapi.parsers import RegExpParser

api = RegExpParser({"digits": r"\d+"}).parse("123abc")
assert api.parse("[a-z]+") == "abc"
```

Pass regular expression flags on parser initialization:

```python
import re

from pyanyapi.parsers import RegExpParser

assert RegExpParser({"test": r"\d+.\d+"}).parse("123\n234").test == "123"
assert RegExpParser({"test": r"\d+.\d+"}, flags=re.DOTALL).parse("123\n234").test == "123\n234"
```

## CSV

Queries have the `row_id:column_id` format:

```python
from pyanyapi.parsers import CSVParser

assert CSVParser({"value": "1:2"}).parse("1,2,3\r\n4,5,6\r\n").value == "6"
```

Extra keyword arguments go to `csv.reader`:

```python
from pyanyapi.parsers import CSVParser

assert CSVParser({"value": "1:2"}, delimiter=";").parse("1;2;3\r\n4;5;6\r\n").value == "6"
```

## AJAX

AJAX responses are often JSON with HTML values:

```python
from pyanyapi.parsers import AJAXParser

api = AJAXParser({"p": "content > string(//p)"}).parse('{"content": "<p>Pcontent</p>"}')
assert api.p == "Pcontent"
```

Queries combine JSON lookups with XPath. Custom queries work too:

```python
from pyanyapi.parsers import AJAXParser

api = AJAXParser().parse('{"content": "<p>Pcontent</p><span>123</span>"}')
assert api.parse("content > string(//span)") == "123"
```

## Index of

Checks whether a string occurs in the content:

```python
from pyanyapi.parsers import IndexOfParser

api = IndexOfParser({"has_bar": "bar", "has_foo": "foo"}).parse("this is bar")
assert api.has_bar is True
assert api.has_foo is False
```

## Custom interface

To declare your own interface, define `execute_method` and, optionally, `perform_parsing`, then create a parser for it.
A naive CSV interface that returns a column value by index:

```python
from typing import Any

from pyanyapi.interfaces import BaseInterface
from pyanyapi.parsers import BaseParser


class CSVInterface(BaseInterface):
    def perform_parsing(self) -> Any:
        return self.content.split(",")

    def execute_method(self, settings: Any) -> Any:
        return self.parsed_content[settings]


class CSVParser(BaseParser):
    interface_class = CSVInterface


assert CSVParser({"second": 1}).parse("1,2,3").second == "2"
```

## Extending interfaces

Parse content with regular Python code using the `interface_method` and `interface_property` decorators.

A custom method:

```python
from pyanyapi.decorators import interface_method
from pyanyapi.parsers import HTMLParser


class ParserWithMethod(HTMLParser):
    settings = {"occupation": "string(.//p/text())"}

    @interface_method
    def hello(self, name):
        return name + " is " + self.occupation


api = ParserWithMethod().parse("<html><body><p>programmer</p></body></html>")
assert api.occupation == "programmer"
assert api.hello("John") == "John is programmer"
```

A custom property:

```python
from pyanyapi.decorators import interface_property
from pyanyapi.parsers import HTMLParser


class ParserWithProperty(HTMLParser):
    settings = {"p": "string(.//p/text())", "h1": "string(.//h1/text())"}

    @interface_property
    def test(self):
        return self.h1 + " " + self.p


api = ParserWithProperty().parse("<html><body><h1>This is</h1><p>test</p></body></html>")
assert api.h1 == "This is"
assert api.p == "test"
assert api.test == "This is test"
```

This example could be a more complex XPath expression, but in general XPath is not enough.
