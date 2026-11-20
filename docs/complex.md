# Complex content

## Combined parsers

When the content type is unknown before parsing, a combined parser tries several parsers transparently.
For example, a server that usually returns JSON, but returns HTML pages on errors:

```python
from pyanyapi.parsers import CombinedParser, HTMLParser, JSONParser


class Parser(CombinedParser):
    parsers = [
        JSONParser({"test": "test"}),
        HTMLParser({"error": "string(//span)"}),
    ]


parser = Parser()
assert parser.parse('{"test": "Text"}').test == "Text"
assert parser.parse("<body><span>123</span></body>").error == "123"
```

The `&` operator combines two parsers:

```python
from pyanyapi.parsers import HTMLParser, JSONParser

parser = JSONParser({"test": "test"}) & HTMLParser({"error": "string(//span)"})
assert parser.parse('{"test": "Text"}').test == "Text"
```

## Mixed content

Different content types can be combined in a single string, often in AJAX responses:

```json
{"content": "<span>Text</span>"}
```

The bundled `AJAXParser` handles it, but the same can be built by hand:

```python
from pyanyapi.decorators import interface_property
from pyanyapi.parsers import HTMLParser, JSONParser

inner_parser = HTMLParser({"text": "string(.//span/text())"})


class CustomAJAXParser(JSONParser):
    settings = {"content": "content"}

    @interface_property
    def text(self):
        return inner_parser.parse(self.content).text


api = CustomAJAXParser().parse('{"content": "<span>Text</span>"}')
assert api.text == "Text"
```

This approach helps to build custom parsers.
