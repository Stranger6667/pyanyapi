from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def interface_property(method: Callable[P, R]) -> "staticmethod[P, R]":
    """Marks method to be included in parsing result as property."""
    method._interface_property = True  # type: ignore[attr-defined]
    return staticmethod(method)


def interface_method(method: Callable[P, R]) -> "staticmethod[P, R]":
    """Marks method to be included in parsing result."""
    method._interface_method = True  # type: ignore[attr-defined]
    return staticmethod(method)
