.. _usage:

Usage
=====

The library provides an ability to create API over various content.
Currently there are bundled tools to work with HTML, XML, CSV, JSON and YAML.
Initially it was created to work with ``requests`` library.

Basic setup
~~~~~~~~~~~

Basic parsers can be declared in the following way:

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    class SimpleParser(HTMLParser):
        settings = {'header': 'string(.//h1/text())'}


    >>> api = SimpleParser().parse('<html><body><h1>Value</h1></body></html>')
    >>> api.header
    Value

Or it can be configured in runtime:

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    >>> api = HTMLParser({
        'header': 'string(.//h1/text())'
    }).parse('<html><body><h1>Value</h1></body></html>')
    >>> api.header
    Value

To get all parsing results as a dict there is ``parse_all`` method.
All properties (include defined with ``@interface_property`` decorator) will be returned.

.. code-block:: python

    from pyanyapi.parsers import JSONParser

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

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    class SimpleParser(HTMLParser):
        settings = {
            'test': {
                'base': '//test',
                'children': 'text()|*//text()'
            }
        }


    >>> api = SimpleParser().parse('<xml><test>123 </test><test><inside> 234</inside></test></xml>')
    >>> api.test
    ['123 ', ' 234']

There is another option to interact with sub-elements. Sub parsers!

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    class SubParser(HTMLParser):
        settings = {
            'href': 'string(//@href)',
            'text': 'string(//text())'
        }


    class Parser(HTMLParser):
        settings = {
            'elem': {
                'base': './/a',
                'parser': SubParser
            }
        }

    >>> api = Parser().parse("<html><body><a href='#test'>test</a></body></html>")
    >>> api.elem[0].href
    #test
    >>> api.elem[0].text
    test
    >>> api.parse_all()
    {'elem': [{'href': '#test', 'text': 'test'}]}

Also you can pass sub parsers as classes or like instances.

Settings inheritance
~~~~~~~~~~~~~~~~~~~~

Settings attribute is merged from all ancestors of current parser.

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


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

.. code-block:: python

    from pyanyapi.parsers import XMLParser


    >>> settings = {'p': 'string(//p)'}
    >>> XMLParser(settings).parse('<p> Pcontent </p>').p
     Pcontent
    >>> XMLParser(settings, strip=True).parse('<p> Pcontent </p>').p
    Pcontent
