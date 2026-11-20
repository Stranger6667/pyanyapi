"""Functions to dynamically attach attributes to classes.

Most of parsing results are cached because of immutability of input data.
"""

from collections.abc import Callable
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class cached_property(Generic[T]):
    """Copied from Django."""

    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func

    def __get__(self, instance: Any, owner: type | None = None) -> T:
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res


def attach_attribute(target: type, name: str, attr: Any) -> None:
    attr.__name__ = name
    attr._attached = True
    setattr(target, name, attr)


def attach_cached_property(target: type, name: str, prop: Callable[[Any], Any]) -> None:
    method = cached_property(prop)
    attach_attribute(target, name, method)
