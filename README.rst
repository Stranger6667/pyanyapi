PyAnyAPI
========

Tools for convenient interface creation over various types of data in
a declarative way.

.. image:: https://travis-ci.org/Stranger6667/pyanyapi.svg?branch=master
   :target: https://travis-ci.org/Stranger6667/pyanyapi
   :alt: Build Status

.. image:: https://codecov.io/github/Stranger6667/pyanyapi/coverage.svg?branch=master
   :target: https://codecov.io/github/Stranger6667/pyanyapi?branch=master
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/pyanyapi/badge/?version=latest
   :target: http://pyanyapi.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

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

The library provides an ability to create API over various content.
Currently there are bundled tools to work with HTML, XML, CSV, JSON and YAML.
Initially it was created to work with ``requests`` library.

Basic parsers can be declared in the following way:

.. code-block:: python

    from pyanyapi.parsers import HTMLParser


    class SimpleParser(HTMLParser):
        settings = {'header': 'string(.//h1/text())'}


    >>> api = SimpleParser().parse('<html><body><h1>Value</h1></body></html>')
    >>> api.header
    Value

Documentation
-------------

You can view documentation online at:

- https://pyanyapi.readthedocs.io

Or you can look at the docs/ directory in the repository.

Python support
--------------

PyAnyAPI supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy and partially PyPy3 and Jython.
Unfortunately ``lxml`` doesn't support PyPy3 and Jython, so HTML & XML parsing is not supported on PyPy3 and Jython.
