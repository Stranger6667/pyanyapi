History
-------

0.5.7 - 28.01.2016
----------------

* Added `parse_all` call on subparsers (#37).

0.5.6 - 24.11.2015
----------------

* Fixed `super` call in exception.

0.5.5 - 23.11.2015
----------------

* Add content to exceptions in case of parsing errors (#35).

0.5.4 - 15.11.2015
----------------

* Fixed `lxml` installation on PyPy (#34).
* Add support for subparsers (#32).

0.5.3 - 30.10.2015
----------------

* Disable stripping in XMLObjectifyParser on PyPy (#30).

0.5.2 - 20.10.2015
----------------

* Fix incorrect stripping in XMLObjectifyParser (#29).

0.5.1 - 20.10.2015
----------------

* Ability to override `strip` attribute at class level (#27).
* Fix `strip` in XMLObjectifyParser (#28).

0.5 - 05.10.2015
----------------

* Add `parse_all` to parse all settings (#20).
* Settings for regular expressions (#19).
* Add `strip` option to strip trailing whitespaces (#14).
* Add CSVParser (#11).

0.4 - 29.09.2015
----------------

* Add YAMLParser (#5).
* Add AJAXParser (#9).
* `parse` calls memoization (#18).

0.3 - 24.09.2015
----------------

* Add partial support for PyPy3 (#7).
* Add partial support for Jython (#6).
* Add ujson as dependency where it is possible (#4).
* Lxml will not be installed where it is not supported (#3).

0.2.1 - 23.09.2015
----------------

* Remove encoding declaration for XMLObjectifyParser

0.2 - 23.09.2015
----------------

* Add ```parse``` methods for JSONInterface & RegExpInterface (#8).
* Add universal wheel config (#2).

0.1 - 22.09.2015
----------------

* First release.