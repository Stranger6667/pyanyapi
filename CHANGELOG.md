# Changelog

## [Unreleased](https://github.com/Stranger6667/pyanyapi/compare/0.6.1...HEAD)

### Added

- Support for Python 3.11–3.15.
- `py.typed` marker.

### Changed

- `lxml` is a required dependency on all platforms.
- JSON is parsed with the standard library `json` module instead of `ujson`.

### Removed

- Support for Python 2.6–3.10 and Jython.

### Fixed

- `XMLObjectifyParser(strip=True)` not stripping nested elements on PyPy and stripping only the first of repeated elements.
- `AJAXParser` raising `TypeError` instead of returning an empty result for queries that do not point to a string with `lxml>=6`.

## 0.6.1 - 2017-11-07

### Fixed

- Arbitrary code execution in `YAMLParser`: content is loaded with `yaml.safe_load` ([#41](https://github.com/Stranger6667/pyanyapi/issues/41)).

## 0.6.0 - 2016-08-09

### Added

- `IndexOfParser`.

## 0.5.8 - 2016-07-14

### Fixed

- XML content parsing for bytes input.

## 0.5.7 - 2016-01-28

### Added

- `parse_all` call on subparsers ([#37](https://github.com/Stranger6667/pyanyapi/issues/37)).

## 0.5.6 - 2015-11-24

### Fixed

- `super` call in exception.

## 0.5.5 - 2015-11-23

### Added

- Content in exceptions in case of parsing errors ([#35](https://github.com/Stranger6667/pyanyapi/issues/35)).

## 0.5.4 - 2015-11-15

### Added

- Support for subparsers ([#32](https://github.com/Stranger6667/pyanyapi/issues/32)).

### Fixed

- `lxml` installation on PyPy ([#34](https://github.com/Stranger6667/pyanyapi/issues/34)).

## 0.5.3 - 2015-10-30

### Changed

- Disable stripping in `XMLObjectifyParser` on PyPy ([#30](https://github.com/Stranger6667/pyanyapi/issues/30)).

## 0.5.2 - 2015-10-20

### Fixed

- Incorrect stripping in `XMLObjectifyParser` ([#29](https://github.com/Stranger6667/pyanyapi/issues/29)).

## 0.5.1 - 2015-10-20

### Added

- Ability to override `strip` attribute at class level ([#27](https://github.com/Stranger6667/pyanyapi/issues/27)).

### Fixed

- `strip` in `XMLObjectifyParser` ([#28](https://github.com/Stranger6667/pyanyapi/issues/28)).

## [0.5](https://github.com/Stranger6667/pyanyapi/compare/0.4...0.5) - 2015-10-05

### Added

- `parse_all` to parse all settings ([#20](https://github.com/Stranger6667/pyanyapi/issues/20)).
- Settings for regular expressions ([#19](https://github.com/Stranger6667/pyanyapi/issues/19)).
- `strip` option to strip trailing whitespaces ([#14](https://github.com/Stranger6667/pyanyapi/issues/14)).
- `CSVParser` ([#11](https://github.com/Stranger6667/pyanyapi/issues/11)).

## [0.4](https://github.com/Stranger6667/pyanyapi/compare/v0.3...0.4) - 2015-09-29

### Added

- `YAMLParser` ([#5](https://github.com/Stranger6667/pyanyapi/issues/5)).
- `AJAXParser` ([#9](https://github.com/Stranger6667/pyanyapi/issues/9)).
- `parse` calls memoization ([#18](https://github.com/Stranger6667/pyanyapi/issues/18)).

## [0.3](https://github.com/Stranger6667/pyanyapi/compare/v0.2.1...v0.3) - 2015-09-24

### Added

- Partial support for PyPy3 ([#7](https://github.com/Stranger6667/pyanyapi/issues/7)).
- Partial support for Jython ([#6](https://github.com/Stranger6667/pyanyapi/issues/6)).
- `ujson` as a dependency where it is possible ([#4](https://github.com/Stranger6667/pyanyapi/issues/4)).

### Changed

- `lxml` is not installed where it is not supported ([#3](https://github.com/Stranger6667/pyanyapi/issues/3)).

## [0.2.1](https://github.com/Stranger6667/pyanyapi/compare/v0.2...v0.2.1) - 2015-09-23

### Fixed

- Remove encoding declaration for `XMLObjectifyParser`.

## [0.2](https://github.com/Stranger6667/pyanyapi/compare/v0.1...v0.2) - 2015-09-23

### Added

- `parse` methods for `JSONInterface` and `RegExpInterface` ([#8](https://github.com/Stranger6667/pyanyapi/issues/8)).
- Universal wheel config ([#2](https://github.com/Stranger6667/pyanyapi/issues/2)).

## 0.1 - 2015-09-22

- Initial release.
