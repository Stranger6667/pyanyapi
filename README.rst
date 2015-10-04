PyAnyAPI
========

Tools for convenient interface creation over various types of data in
declarative way.

|Build Status| |codecov.io|

Installation
------------

The current stable release:

::

    pip install pyanyapi

or:

::

    easy_install pyanyapi

or from source:

::

    $ sudo python setup.py install

Usage
-----

Library provides an ability to create API over various content.
Currently there are bundled tools to work with HTML, XML, CSV, JSON and YAML.
Initially it was created to work with ``requests`` library.

Basic setup
~~~~~~~~~~~

Basic parsers can be declared in following way:

.. code:: python

    from pyanyapi import HTMLParser


    class SimpleParser(HTMLParser):
        settings = {'header': 'string(.//h1/text())'}


    >>> api = SimpleParser().parse('<html><body><h1>Value</h1></body></html>')
    >>> api.header
    Value

Or it can be configured in runtime:

.. code:: python

    from pyanyapi import HTMLParser


    >>> api = HTMLParser({'header': 'string(.//h1/text())'}).parse('<html><body><h1>Value</h1></body></html>')
    >>> api.header
    Value

To get all parsing results as a dict there is ``parse_all`` method.
All properties (include defined with ``@interface_property`` decorator) will be returned.

.. code:: python

    from pyanyapi import JSONParser

    >>> JSONParser({
        'first': 'container > 0',
        'second': 'container > 1',
        'third': 'container > 2',
    }).parse('{"container":["first", "second", "third"]}').parse_all()
    {
        'first': 'first',
        'second': 'second',
        'third': 'third',
    }

Complex setup
~~~~~~~~~~~~~

In some cases you may want to apply extra transformations to result
list. Here comes "base-children" setup style.

.. code:: python

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

Settings inheritance
~~~~~~~~~~~~~~~~~~~~

Settings attribute is merged from all ancestors of current parser.

.. code:: python

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

Results stripping
~~~~~~~~~~~~~~~~~

Parsers can automagically strip trailing whitespaces with ``strip=True`` option.

.. code:: python

    from pyanyapi import RegExpParser


    >>> settings = {'p': 'string(//p)'}
    >>> XMLParser(settings).parse('<p> Pcontent </p>').p
     Pcontent
    >>> XMLParser(settings, strip=True).parse('<p> Pcontent </p>).p
    Pcontent

HTML & XML
~~~~~~~~~~

For HTML and XML based interfaces XPath 1.0 syntax is used for settings
declaration. Unfortunately XPath 2.0 is not supported by lxml. XML is
about the same as HTMLParser, but uses different lxml parser internally.
Here is an example of usage with ``requests``:

.. code:: python

    >>> import requests
    >>> import pyanyapi
    >>> parser = pyanyapi.HTMLParser({'header': 'string(.//h1/text())'}) 
    >>> response = requests.get('http://example.com')
    >>> api = parser.parse(response.text)
    >>> api.header
    Example Domain

If you need, you can execute more XPath queries at any time you want:

.. code:: python

    from pyanyapi import HTMLParser


    >>> parser = HTMLParser({'header': 'string(.//h1/text())'})
    >>> api = parser.parse('<html><body><h1>This is</h1><p>test</p></body></html>')
    >>> api.header
    This is
    >>> api.parse('string(//p)')
    test

XML Objectify
~~~~~~~~~~~~~

Lxml provide interesting feature - objectified interface for XML. It
converts whole XML to Python object. This parser doesn't require any
settings. E.g:

.. code:: python

    from pyanyapi import XMLObjectifyParser


    >>> XMLObjectifyParser().parse('<xml><test>123</test></xml>').test
    123

JSON
~~~~

Settings syntax in based on PostgreSQL statements syntax.

.. code:: python

    from pyanyapi import JSONParser
     
     
    >>> JSONParser({'id': 'container > id'}).parse('{"container":{"id":"123"}}').id
    123

Or you can access values in lists by index:

.. code:: python

    from pyanyapi import JSONParser
     
     
    >>> JSONParser({'second': 'container > 1'}).parse('{"container":["first", "second", "third"]}').second
    second

And executes more queries after initial parsing:

.. code:: python

    from pyanyapi import JSONParser
     
     
    >>> api = JSONParser({'second': 'container > 1'}).parse('{"container":[],"second_container":[123]}')
    >>> api.parse('second_container > 0')
    123

YAML
~~~~
Equal to JSON parser, but works with YAML data.

.. code:: python

    from pyanyapi import YAMLParser


    >>> YAMLParser({'test': 'container > test'}).parse('container:\n    test: "123"').test
    123

Regular Expressions Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case, when data has bad format or is just very complex to be parsed
with bundled tools, you can use parser based on regular expressions.
Settings is based on Python's regular expressions. It is most powerful
parser, because of its simplicity.

.. code:: python

    from pyanyapi import RegExpParser


    >>> RegExpParser({'error_code': 'Error (\d+)'}).parse('Oh no!!! It is Error 100!!!').error_code
    100

And executes more queries after initial parsing:

.. code:: python

    from pyanyapi import RegExpParser


    >>> api = RegExpParser({'digits': '\d+'}).parse('123abc')
    >>> api.parse('[a-z]+')
    abc

Also, you can pass flags for regular expressions on parser initialization:

.. code:: python

    from pyanyapi import RegExpParser


    >>> RegExpParser({'test': '\d+.\d+'}).parse('123\n234').test
    123
    >>> RegExpParser({'test': '\d+.\d+'}, flags=re.DOTALL).parse('123\n234').test
    123
    234


CSV Interface
~~~~~~~~~~~~~

Operates with CSV data with simple queries in format 'row_id:column_id'.

.. code:: python

    from pyanyapi import CSVParser


    >>> CSVParser({'value': '1:2'}).parse('1,2,3\r\n4,5,6\r\n').value
    6

Also, you can pass custom kwargs for `csv.reader` on parser initialization:

.. code:: python

    from pyanyapi import CSVParser


    >>> CSVParser({'value': '1:2'}, delimiter=';').parse('1;2;3\r\n4;5;6\r\n').value
    6

AJAX Interface
~~~~~~~~~~~~~~

AJAX is very popular technology and often use JSON data with HTML values. Here is an example:

.. code:: python

    from pyanyapi import AJAXParser


    >>> api = AJAXParser({'p': 'content > string(//p)'}).parse('{"content": "<p>Pcontent</p>"}')
    >>> api.p
    Pcontent

It use combination of XPath queries and PostgreSQL-based JSON lookups.
Custom queries execution is also available:

.. code:: python

    from pyanyapi import AJAXParser


    >>> api = AJAXParser().parse('{"content": "<p>Pcontent</p><span>123</span>"}')
    >>> api.parse('content > string(//span)')
    123


Custom Interface
~~~~~~~~~~~~~~~~

You can easily declare your own interface. For that you should define
``execute_method`` method. And optionally ``perform_parsing``. Here is
an example of naive CSVInterface, which provide an ability to get column
value by index. Also you should create separate parser for that.

.. code:: python

    from pyanyapi import BaseInterface, BaseParser


    class CSVInterface(BaseInterface):

        def perform_parsing(self):
            return self.content.split(',')

        def execute_method(self, settings):
            return self.parsed_content[settings]


    class CSVParser(BaseParser):
        interface_class = CSVInterface


    >>> CSVParser({'second': 1}).parse('1,2,3').second
    2

Extending interfaces
--------------------

Also content can be parsed with regular Python code. It can be done with
special decorators ``interface_method`` and ``interface_property``.

Custom method example:

.. code:: python

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

Custom property example:

.. code:: python

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

Certainly previous example can be done with more complex XPath
expression, but in general case XPath is not enough.

Complex content parsing
-----------------------

Combined parsers
~~~~~~~~~~~~~~~~

In situations, when particular content type is unknown before parsing,
you can create combined parser, which allows you to use multiply
different parsers transparently. E.g. some server usually returns JSON,
but in cases of server errors it returns HTML pages with some text.
Then:

.. code:: python

    from pyanyapi import CombinedParser, HTMLParser, JSONParser


    class Parser(CombinedParser):
        parsers = [
            JSONParser({'test': 'test'}),
            HTMLParser({'error': 'string(//span)'})
        ]

    >>> parser = Parser()
    >>> parser.parse('{"test": "Text"}').content
    Text
    >>> parser.parse('<body><span>123</span></body>').error
    123

Another example
~~~~~~~~~~~~~~~

Sometimes different content types can be combined inside single string.
Often with AJAX requests.

.. code:: javascript

    {"content": "<span>Text</span>"}

You can work with such data in following way:

.. code:: python

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

Now AJAXParser is bundled in pyanyapi, but it works different.
But anyway this example can be helpful for building custom parsers.

Python support
--------------

PyAnyAPI supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy and partially PyPy3 and Jython.
Unfortunately ``lxml`` doesn't support PyPy3 and Jython, so HTML & XML parsing is not supported on PyPy3 and Jython.

.. |Build Status| image:: https://travis-ci.org/Stranger6667/pyanyapi.svg
   :target: https://travis-ci.org/Stranger6667/pyanyapi
.. |codecov.io| image:: http://codecov.io/github/Stranger6667/pyanyapi/coverage.svg?branch=master
   :target: http://codecov.io/github/Stranger6667/pyanyapi?branch=master
