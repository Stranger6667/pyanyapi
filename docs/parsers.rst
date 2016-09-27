.. _parsers:

Parsers
=======

HTML & XML
~~~~~~~~~~

For HTML and XML based interfaces XPath 1.0 syntax is used for settings
declaration. Unfortunately XPath 2.0 is not supported by lxml. XML is
about the same as HTMLParser, but uses a different lxml parser internally.
Here is an example of usage with ``requests``:

.. code-block:: python

    >>> import requests
    >>> import pyanyapi
    >>> parser = pyanyapi.HTMLParser({'header': 'string(.//h1/text())'})
    >>> response = requests.get('http://example.com')
    >>> api = parser.parse(response.text)
    >>> api.header
    Example Domain

If you need, you can execute more XPath queries at any time you want:

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    >>> parser = HTMLParser({'header': 'string(.//h1/text())'})
    >>> api = parser.parse('<html><body><h1>This is</h1><p>test</p></body></html>')
    >>> api.header
    This is
    >>> api.parse('string(//p)')
    test

XML Objectify
~~~~~~~~~~~~~

Lxml provides interesting feature - objectified interface for XML. It
converts whole XML to Python object. This parser doesn't require any
settings. E.g:

.. code-block:: python

    from pyanyapi.parsers import XMLObjectifyParser


    >>> XMLObjectifyParser().parse('<xml><test>123</test></xml>').test
    123

JSON
~~~~

Settings syntax in based on PostgreSQL statements syntax.

.. code-block:: python

    from pyanyapi.parsers import JSONParser


    >>> JSONParser({'id': 'container > id'}).parse('{"container":{"id":"123"}}').id
    123

Or you can get access to values in lists by index:

.. code-block:: python

    from pyanyapi.parsers import JSONParser


    >>> JSONParser({'second': 'container > 1'}).parse('{"container":["first", "second", "third"]}').second
    second

And executes more queries after initial parsing:

.. code-block:: python

    from pyanyapi.parsers import JSONParser


    >>> api = JSONParser({'second': 'container > 1'}).parse('{"container":[],"second_container":[123]}')
    >>> api.parse('second_container > 0')
    123

YAML
~~~~
Equal to JSON parser, but works with YAML data.

.. code-block:: python

    from pyanyapi.parsers import YAMLParser


    >>> YAMLParser({'test': 'container > test'}).parse('container:\n    test: "123"').test
    123

Regular Expressions Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case, when data has wrong format or is just very complicated to be parsed
with bundled tools, you can use a parser based on regular expressions.
Settings are based on Python's regular expressions. It is the most powerful
parser, because of its simplicity.

.. code-block:: python

    from pyanyapi.parsers import RegExpParser


    >>> RegExpParser({'error_code': 'Error (\d+)'}).parse('Oh no!!! It is Error 100!!!').error_code
    100

And executes more queries after initial parsing:

.. code-block:: python

    from pyanyapi.parsers import RegExpParser


    >>> api = RegExpParser({'digits': '\d+'}).parse('123abc')
    >>> api.parse('[a-z]+')
    abc

Also, you can pass flags for regular expressions on parser initialization:

.. code-block:: python

    from pyanyapi.parsers import RegExpParser


    >>> RegExpParser({'test': '\d+.\d+'}).parse('123\n234').test
    123
    >>> RegExpParser({'test': '\d+.\d+'}, flags=re.DOTALL).parse('123\n234').test
    123
    234


CSV Interface
~~~~~~~~~~~~~

Operates with CSV data with simple queries in format 'row_id:column_id'.

.. code-block:: python

    from pyanyapi.parsers import CSVParser


    >>> CSVParser({'value': '1:2'}).parse('1,2,3\r\n4,5,6\r\n').value
    6

Also, you can pass custom kwargs for `csv.reader` on parser initialization:

.. code-block:: python

    from pyanyapi.parsers import CSVParser


    >>> CSVParser({'value': '1:2'}, delimiter=';').parse('1;2;3\r\n4;5;6\r\n').value
    6

AJAX Interface
~~~~~~~~~~~~~~

AJAX is a very popular technology and often use JSON data with HTML values. Here is an example:

.. code-block:: python

    from pyanyapi.parsers import AJAXParser


    >>> api = AJAXParser({'p': 'content > string(//p)'}).parse('{"content": "<p>Pcontent</p>"}')
    >>> api.p
    Pcontent

It uses combination of XPath queries and PostgreSQL-based JSON lookups.
Custom queries execution is also available:

.. code-block:: python

    from pyanyapi.parsers import AJAXParser


    >>> api = AJAXParser().parse('{"content": "<p>Pcontent</p><span>123</span>"}')
    >>> api.parse('content > string(//span)')
    123


Custom Interface
~~~~~~~~~~~~~~~~

You can easily declare your own interface. For that you should define
``execute_method`` method. And optionally ``perform_parsing``. Here is
an example of naive CSVInterface, which provides an ability to get the column
value by index. Also you should create a separate parser for that.

.. code-block:: python

    from pyanyapi.interfaces import BaseInterface
    from pyanyapi.parsers import BaseParser


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
~~~~~~~~~~~~~~~~~~~~

Also content can be parsed with regular Python code. It can be done with
special decorators ``interface_method`` and ``interface_property``.

Custom method example:

.. code-block:: python

    from pyanyapi.decorators import interface_method
    from pyanyapi.parsers import interface_method


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

.. code-block:: python

    from pyanyapi.decorators import interface_property
    from pyanyapi.parsers import HTMLParser


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

Certainly the previous example can be done with more complex XPath
expression, but in general case XPath is not enough.
