# Usage

PyAnyAPI creates an API over various content.
It bundles parsers for HTML, XML, CSV, JSON and YAML.
It was initially created to work with the `requests` library.

## Basic setup

Declare a parser as a class:

```python
from pyanyapi.parsers import HTMLParser


class SimpleParser(HTMLParser):
    settings = {"header": "string(.//h1/text())"}


api = SimpleParser().parse("<html><body><h1>Value</h1></body></html>")
assert api.header == "Value"
```

Or configure it at runtime:

```python
from pyanyapi.parsers import HTMLParser

api = HTMLParser({"header": "string(.//h1/text())"}).parse("<html><body><h1>Value</h1></body></html>")
assert api.header == "Value"
```

`parse_all` returns all parsing results as a dict, including properties defined with `@interface_property`:

```python
from pyanyapi.parsers import JSONParser

api = JSONParser(
    {
        "first": "container > 0",
        "second": "container > 1",
        "third": "container > 2",
    }
).parse('{"container": ["first", "second", "third"]}')
assert api.parse_all() == {"first": "first", "second": "second", "third": "third"}
```

## Complex setup

To apply extra transformations to a result list, use the "base-children" style:

```python
from pyanyapi.parsers import XMLParser


class SimpleParser(XMLParser):
    settings = {
        "test": {
            "base": "//test",
            "children": "text()|*//text()",
        }
    }


api = SimpleParser().parse("<xml><test>123 </test><test><inside> 234</inside></test></xml>")
assert api.test == ["123 ", " 234"]
```

Sub-parsers process each element of a result list:

```python
from pyanyapi.parsers import HTMLParser


class SubParser(HTMLParser):
    settings = {
        "href": "string(//@href)",
        "text": "string(//text())",
    }


class Parser(HTMLParser):
    settings = {
        "elem": {
            "base": ".//a",
            "parser": SubParser,
        }
    }


api = Parser().parse("<html><body><a href='#test'>test</a></body></html>")
assert api.elem[0].href == "#test"
assert api.elem[0].text == "test"
assert api.parse_all() == {"elem": [{"href": "#test", "text": "test"}]}
```

A sub-parser can be a class or an instance.

## Settings inheritance

The `settings` attribute is merged from all ancestors of the parser:

```python
from pyanyapi.parsers import HTMLParser


class ParentParser(HTMLParser):
    settings = {"parent": "//p"}


class FirstChildParser(ParentParser):
    settings = {"parent": "//override"}


class SecondChildParser(ParentParser):
    settings = {"child": "//h1"}


assert FirstChildParser().settings["parent"] == "//override"
assert SecondChildParser().settings["parent"] == "//p"
assert SecondChildParser().settings["child"] == "//h1"
assert SecondChildParser({"child": "//more"}).settings["child"] == "//more"
```

## Results stripping

With `strip=True`, parsers strip leading and trailing whitespace from results:

```python
from pyanyapi.parsers import XMLParser

settings = {"p": "string(//p)"}
assert XMLParser(settings).parse("<p> Pcontent </p>").p == " Pcontent "
assert XMLParser(settings, strip=True).parse("<p> Pcontent </p>").p == "Pcontent"
```
