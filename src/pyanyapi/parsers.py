"""Classes for fabrics of interfaces.

Generates interfaces dynamically from given settings.
"""

from collections.abc import Sequence
from typing import Any

from .helpers import attach_attribute, attach_cached_property
from .interfaces import (
    AJAXInterface,
    BaseInterface,
    CombinedInterface,
    CSVInterface,
    IndexOfInterface,
    JSONInterface,
    RegExpInterface,
    XMLInterface,
    XMLObjectifyInterface,
    XPathInterface,
    YAMLInterface,
)


class BaseParser:
    """Fabric for some API-like components, which supposes to provide interface to different types of content."""

    interface_class: type[BaseInterface]
    settings: dict[str, Any]
    strip = False

    def __init__(self, settings: dict[str, Any] | None = None, strip: bool | None = None) -> None:
        if strip is not None:
            self.strip = strip
        parents_settings = self.get_parents_settings()
        if settings:
            parents_settings.update(settings)
        self.settings = parents_settings

    @property
    def attributes(self) -> list[str]:
        extra_attributes = []
        for name in dir(self):
            if name == "attributes":
                continue
            attr = getattr(self, name)
            if hasattr(attr, "_interface_property") or hasattr(attr, "_interface_method"):
                extra_attributes.append(name)
        return list(self.settings.keys()) + extra_attributes

    def get_parents_settings(self) -> dict[str, Any]:
        """Gather settings from parent classes. It provides some kind of settings inheritance."""
        parents_settings: dict[str, Any] = {}
        for klass in reversed(self.__class__.mro()):
            parents_settings.update(getattr(klass, "settings", {}))
        return parents_settings

    def parse(self, content: Any = "") -> BaseInterface:
        """Generates new class instance with desired attributes."""
        self.content = self.prepare_content(content)

        Interface: type[BaseInterface] = type("Interface", (self.interface_class,), {})
        self.setup_class(Interface)

        init_kwargs = self.get_interface_kwargs()

        return Interface(**init_kwargs)

    def parse_all(self, content: Any = "") -> dict[str, Any]:
        return self.parse(content).parse_all()

    def get_interface_kwargs(self) -> dict[str, Any]:
        return {"content": self.content, "strip": self.strip}

    def prepare_content(self, content: Any) -> Any:
        """Hook to provide way to transform content."""
        return content

    def setup_class(self, cls: type[BaseInterface]) -> None:
        """Attaches dynamic properties & methods."""
        self.process_settings(cls)
        self.process_decorators(cls)

    def process_settings(self, cls: type[BaseInterface]) -> None:
        """Generates methods, based on settings."""
        for name, settings in self.settings.items():
            attr = cls.init_attr(settings)
            attach_cached_property(cls, name, attr)

    def process_decorators(self, cls: type[BaseInterface]) -> None:
        """Re-attach all attributes decorated with `@interface_property` or `@interface_method` to the new class."""
        for name in dir(self):
            attr = getattr(self, name)
            if getattr(attr, "_interface_property", False):
                attach_cached_property(cls, name, attr)
            elif getattr(attr, "_interface_method", False):
                attach_attribute(cls, name, attr)

    def __and__(self, other: "BaseParser") -> "CombinedParser":
        return CombinedParser(self, other)


class CombinedParser(BaseParser):
    """Combines multiple parsers in one. This can also be in different types."""

    interface_class = CombinedInterface
    parsers: Sequence[BaseParser]

    def __init__(self, *parsers: BaseParser, settings: dict[str, Any] | None = None, strip: bool | None = None) -> None:
        if parsers:
            self.parsers = parsers
        super().__init__(settings, strip)

    @property
    def attributes(self) -> list[str]:
        return super().attributes + [name for parser in self.parsers for name in parser.attributes]

    def get_interface_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_interface_kwargs()
        kwargs["parsers"] = self.parsers
        return kwargs


class HTMLParser(BaseParser):
    interface_class = XPathInterface


class XMLParser(BaseParser):
    interface_class: type[BaseInterface] = XMLInterface

    def prepare_content(self, content: Any) -> Any:
        if isinstance(content, bytes):
            return content.replace(b'encoding="UTF-8"', b"").replace(b'encoding="utf-8"', b"")
        return content.replace('encoding="UTF-8"', "").replace('encoding="utf-8"', "")


class XMLObjectifyParser(XMLParser):
    interface_class = XMLObjectifyInterface


class JSONParser(BaseParser):
    interface_class = JSONInterface


class YAMLParser(BaseParser):
    interface_class = YAMLInterface


class AJAXParser(BaseParser):
    interface_class = AJAXInterface


class RegExpParser(BaseParser):
    interface_class = RegExpInterface

    def __init__(self, settings: dict[str, Any] | None = None, strip: bool | None = None, flags: int = 0) -> None:
        self.flags = flags
        super().__init__(settings, strip)

    def get_interface_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_interface_kwargs()
        kwargs["flags"] = self.flags
        return kwargs


class CSVParser(BaseParser):
    interface_class = CSVInterface

    def __init__(self, settings: dict[str, Any] | None = None, strip: bool | None = None, **reader_kwargs: Any) -> None:
        self.reader_kwargs = reader_kwargs
        super().__init__(settings, strip)

    def get_interface_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_interface_kwargs()
        kwargs.update(self.reader_kwargs)
        return kwargs


class IndexOfParser(BaseParser):
    interface_class = IndexOfInterface

    def prepare_content(self, content: Any) -> Any:
        if isinstance(content, bytes):
            return content.decode()
        return content
