# PyAnyAPI

[![Build](https://github.com/Stranger6667/pyanyapi/actions/workflows/build.yml/badge.svg)](https://github.com/Stranger6667/pyanyapi/actions/workflows/build.yml)
[![Coverage](https://codecov.io/github/Stranger6667/pyanyapi/coverage.svg?branch=master)](https://codecov.io/github/Stranger6667/pyanyapi?branch=master)
[![Version](https://img.shields.io/pypi/v/pyanyapi.svg)](https://pypi.org/project/pyanyapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyanyapi.svg)](https://pypi.org/project/pyanyapi/)
[![Docs](https://readthedocs.org/projects/pyanyapi/badge/?version=stable)](https://pyanyapi.readthedocs.io/en/stable/)
[![License](https://img.shields.io/pypi/l/pyanyapi.svg)](https://opensource.org/licenses/MIT)

Tools for convenient interface creation over various types of data in a declarative way.

Declare the attributes you need as queries, and PyAnyAPI turns the content into an object with those attributes:
XPath for HTML and XML, `container > key` lookups for JSON and YAML, `row:column` for CSV and regular expressions for text.

## Installation

```
uv pip install pyanyapi
```

## Usage

```python
from pyanyapi.parsers import HTMLParser


class SimpleParser(HTMLParser):
    settings = {"header": "string(.//h1/text())"}


api = SimpleParser().parse("<html><body><h1>Value</h1></body></html>")
assert api.header == "Value"
```

JSON lookups and all results at once:

```python
from pyanyapi.parsers import JSONParser

api = JSONParser({"id": "container > id", "second": "items > 1"}).parse(
    '{"container": {"id": "123"}, "items": ["first", "second"]}'
)
assert api.parse_all() == {"id": "123", "second": "second"}
```

Combine parsers when the content type is unknown upfront, e.g. JSON responses with HTML error pages:

```python
from pyanyapi.parsers import HTMLParser, JSONParser

parser = JSONParser({"status": "status"}) & HTMLParser({"error": "string(//h1)"})
assert parser.parse('{"status": "ok"}').status == "ok"
assert parser.parse("<html><body><h1>Server error</h1></body></html>").error == "Server error"
```

## Features

- Parsers for HTML, XML, XML Objectify, JSON, YAML, CSV, AJAX (JSON with HTML values), regular expressions and substring checks.
- Settings inheritance, sub-parsers and "base-children" queries for result lists.
- Custom properties and methods via `@interface_property` and `@interface_method`.
- Optional stripping of whitespace in results.
- Type annotations, with a `py.typed` marker.

## Documentation

<https://pyanyapi.readthedocs.io/en/stable/>

## Python support

PyAnyAPI supports CPython 3.11 to 3.15 and PyPy 3.11.
