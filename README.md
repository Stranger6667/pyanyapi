PyAnyAPI
========
Tools for convenient interface creation over various types of data in declarative way.

[![Build Status](https://travis-ci.org/Stranger6667/pyanyapi.svg)](https://travis-ci.org/Stranger6667/pyanyapi)
[![codecov.io](http://codecov.io/github/Stranger6667/pyanyapi/coverage.svg?branch=master)](http://codecov.io/github/Stranger6667/pyanyapi?branch=master)

Installation
------------

The current stable release:

    pip install pyanyapi

or:

    easy_install pyanyapi
    
or from source:

    $ sudo python setup.py install

Usage
-----

Library provides an ability to create API over various content. Currently there are bundled tools to work with HTML, XML, JSON.
Initially it was created to work with ```requests``` library.

### Basic setup

Basic parsers can be declared in following way:

```Python
from pyanyapi import HTMLParser


class SimpleParser(HTMLParser):
    settings = {'header': 'string(.//h1/text())'}


>>> api = SimpleParser().parse('<html><body><h1>Value</h1></body></html>')
>>> api.header
Value
```

Or it can be configured in runtime:
```Python
from pyanyapi import HTMLParser


>>> api = HTMLParser({'header': 'string(.//h1/text())'}).parse('<html><body><h1>Value</h1></body></html>')
>>> api.header
Value
```

### Complex setup

In some cases you may want to apply extra transformations to result list. Here comes "base-children" setup style.

```Python
from pyanyapi import HTMLParser


class SimpleParser(HTMLParser):
    settings = {
        'header': {
            'base': '//test', 
            'children': 'text()|*//text()'
        }
    }


>>> api = SimpleParser().parse('<xml><test>123 </test><test><inside> 234</inside></test></xml>')
>>> api.test
['123', '234']
```

### Settings inheritance

Settings attribute is merged from all ancestors of current parser.

```Python
from pyanyapi import HTMLParser


class ParentParser(HTMLParser):
    settings = {'parent': '//p'}


class FirstChildParser(ParentParser):
    settings = {'parent': '//override'}


class SecondChildParser(ParentParser):
    settings = {'child': '//h1'}


>>> FirstChildParser().settings['parent']
//override

>>> SecondChildParser().settings['parent']
//p

>>> SecondChildParser().settings['child']
//h1

>>> SecondChildParser({'child': '//more'}).settings['child']
//more
```

### HTML & XML

Here is an example of usage with ```requests```:

```Python
>>> import requests
>>> import pyanyapi
>>> parser = pyanyapi.HTMLParser({'header': 'string(.//h1/text())'}) 
>>> response = requests.get('http://example.com')
>>> api = parser.parse(response.text)
>>> api.header
Example Domain
```

For HTML and XML based interfaces XPath 1.0 syntax is used for settings declaration. Unfortunately XPath 2.0 is not supported by lxml.
XML is about the same as HTMLParser, but uses different lxml parser internally. 

### JSON

Settings syntax in based on PostgreSQL statements syntax.

```Python
from pyanyapi import JSONParser
 
 
>>> JSONParser({'id': 'container > id'}).parse('{"container":{"id":"123"}}').id
123
```

### Regular Expressions Interface

In case, when data has bad format or is just very complex to be parsed with bundled tools, you can use parser based on regular expressions.
Settings is based on Python's regular expressions. It is most powerful parser, because of its simplicity.


```Python
from pyanyapi import RegExpResponseParser

>>> RegExpResponseParser({'error_code': 'Error (\d+)'}).parse('Oh no!!! It is Error 100!!!').error_code
100
```
### Custom Interface

You can easily declare your own interface.


Extending interfaces
--------------------

Also content can be parsed with regular Python code. It can be done with special decorators ```interface_method``` and ```interface_property```.

Custom method example:

```Python
from pyanyapi import HTMLParser, interface_method


class ParserWithMethod(HTMLParser):
    settings = {'occupation': 'string(.//p/text())'}

    @interface_method
    def hello(self, name):
        return name + ' is ' + self.occupation


>>> api = ParserWithMethod().parse('<html><body><p>programmer</p></body></html>')
>>> api.occupation
programmer

>>> api.hello('John')
John is programmer

```

Custom property example:

```Python
from pyanyapi import HTMLParser, interface_property


class ParserWithProperty(HTMLParser):
    settings = {'p': 'string(.//p/text())', 'h1': 'string(.//h1/text())'}

    @interface_property
    def test(self):
        return self.h1 + ' ' + self.p


>>> api = ParserWithProperty().parse('<html><body><h1>This is</h1><p>test</p></body></html>')
>>> api.h1
This is

>>> api.p
test

>>> api.test
This is test
```

Certainly previous example can be done with more complex XPath expression, but in general case XPath is not enough.

Complex content parsing
-----------------------

### Combined parsers

In situations, when particular content type is unknown before parsing, you can create combined parser, which allows you to use multiply different parsers transparently.

### Another example

Sometimes different content types can be combined inside single string. Often with AJAX requests.

```JavaScript
{"content": "<span>Text</span>"}
```

You can work with such data in following way:
```Python
from pyanyapi import HTMLParser, JSONParser, interface_property


inner_parser = HTMLParser({'text': 'string(.//span/text())'})


class AJAXParser(JSONParser):
    settings = {'content': 'content'}

    @interface_property
    def text(self):
        return inner_parser.parse(self.content).text


>>> api = AJAXParser().parse('{"content": "<span>Text</span>"}')
>>> api.text
Text
```

Probably such parser will be bundled in library in future.

Python support
--------------
PyAnyAPI supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5 and PyPy. Unfortunately PyPy3 is not supported because of ```lxml``` compatibility.
In future release ```lxml``` will become optional, which allows library to be partially used with PyPy3 or Jython. 