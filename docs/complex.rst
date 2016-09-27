.. _complex:

Complex content parsing
=======================

Combined parsers
~~~~~~~~~~~~~~~~

In situations, when particular content type is unknown before parsing,
you can create combined parser, which allows you to use multiply
different parsers transparently. E.g. some server usually returns JSON,
but in cases of server errors it returns HTML pages with some text.
Then:

.. code-block:: python

    from pyanyapi.parsers import CombinedParser, HTMLParser, JSONParser


    class Parser(CombinedParser):
        parsers = [
            JSONParser({'test': 'test'}),
            HTMLParser({'error': 'string(//span)'})
        ]

    >>> parser = Parser()
    >>> parser.parse('{"test": "Text"}').test
    Text
    >>> parser.parse('<body><span>123</span></body>').error
    123

Another example
~~~~~~~~~~~~~~~

Sometimes different content types can be combined inside single string.
Often with AJAX requests.

.. code:: javascript

    {"content": "<span>Text</span>"}

You can work with such data in the following way:

.. code-block:: python

    from pyanyapi.decorators import interface_property
    from pyanyapi.parsers import HTMLParser, JSONParser


    inner_parser = HTMLParser({'text': 'string(.//span/text())'})


    class AJAXParser(JSONParser):
        settings = {'content': 'content'}

        @interface_property
        def text(self):
            return inner_parser.parse(self.content).text


    >>> api = AJAXParser().parse('{"content": "<span>Text</span>"}')
    >>> api.text
    Text

Now AJAXParser is bundled in pyanyapi, but it works differently.
But anyway, this example can be helpful for building custom parsers.