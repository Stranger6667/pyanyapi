.. _changelog:

Changelog
=========

0.6.0 - 09.08.2016
------------------

* IndexOf parser.

0.5.8 - 14.07.2016
------------------

* Fixed XML content parsing for bytes input.

0.5.7 - 28.01.2016
------------------

* Added ``parse_all`` call on subparsers (`#37`_).

0.5.6 - 24.11.2015
------------------

* Fixed ``super`` call in exception.

0.5.5 - 23.11.2015
------------------

* Add content to exceptions in case of parsing errors (`#35`_).

0.5.4 - 15.11.2015
------------------

* Fixed ``lxml`` installation on PyPy (`#34`_).
* Add support for subparsers (`#32`_).

0.5.3 - 30.10.2015
------------------

* Disable stripping in XMLObjectifyParser on PyPy (`#30`_).

0.5.2 - 20.10.2015
------------------

* Fix incorrect stripping in XMLObjectifyParser (`#29`_).

0.5.1 - 20.10.2015
------------------

* Ability to override ``strip`` attribute at class level (`#27`_).
* Fix ``strip`` in XMLObjectifyParser (`#28`_).

0.5 - 05.10.2015
----------------

* Add ``parse_all`` to parse all settings (`#20`_).
* Settings for regular expressions (`#19`_).
* Add ``strip`` option to strip trailing whitespaces (`#14`_).
* Add CSVParser (`#11`_).

0.4 - 29.09.2015
----------------

* Add YAMLParser (`#5`_).
* Add AJAXParser (`#9`_).
* ``parse`` calls memoization (`#18`_).

0.3 - 24.09.2015
----------------

* Add partial support for PyPy3 (`#7`_).
* Add partial support for Jython (`#6`_).
* Add ujson as dependency where it is possible (`#4`_).
* Lxml will not be installed where it is not supported (`#3`_).

0.2.1 - 23.09.2015
------------------

* Remove encoding declaration for XMLObjectifyParser

0.2 - 23.09.2015
----------------

* Add ``parse`` methods for JSONInterface & RegExpInterface (`#8`_).
* Add universal wheel config (`#2`_).

0.1 - 22.09.2015
----------------

* First release.

.. _#37: https://github.com/Stranger6667/pyanyapi/issues/37
.. _#35: https://github.com/Stranger6667/pyanyapi/issues/35
.. _#34: https://github.com/Stranger6667/pyanyapi/issues/34
.. _#32: https://github.com/Stranger6667/pyanyapi/issues/32
.. _#30: https://github.com/Stranger6667/pyanyapi/issues/30
.. _#29: https://github.com/Stranger6667/pyanyapi/issues/29
.. _#28: https://github.com/Stranger6667/pyanyapi/issues/28
.. _#27: https://github.com/Stranger6667/pyanyapi/issues/27
.. _#20: https://github.com/Stranger6667/pyanyapi/issues/20
.. _#19: https://github.com/Stranger6667/pyanyapi/issues/19
.. _#18: https://github.com/Stranger6667/pyanyapi/issues/18
.. _#14: https://github.com/Stranger6667/pyanyapi/issues/14
.. _#11: https://github.com/Stranger6667/pyanyapi/issues/11
.. _#9: https://github.com/Stranger6667/pyanyapi/issues/9
.. _#8: https://github.com/Stranger6667/pyanyapi/issues/8
.. _#7: https://github.com/Stranger6667/pyanyapi/issues/7
.. _#6: https://github.com/Stranger6667/pyanyapi/issues/6
.. _#5: https://github.com/Stranger6667/pyanyapi/issues/5
.. _#4: https://github.com/Stranger6667/pyanyapi/issues/4
.. _#3: https://github.com/Stranger6667/pyanyapi/issues/3
.. _#2: https://github.com/Stranger6667/pyanyapi/issues/2