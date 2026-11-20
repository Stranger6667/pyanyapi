# PyAnyAPI

Tools for convenient interface creation over various types of data in a declarative way.

PyAnyAPI turns HTML, XML, JSON, YAML, CSV, AJAX responses and plain text into objects whose attributes are declared as queries:
XPath for HTML and XML, `container > key` lookups for JSON and YAML, regular expressions for text.

```
uv pip install pyanyapi
```

```python
from pyanyapi.parsers import HTMLParser


class SimpleParser(HTMLParser):
    settings = {"header": "string(.//h1/text())"}


api = SimpleParser().parse("<html><body><h1>Value</h1></body></html>")
assert api.header == "Value"
```
