# coding: utf-8
"""
Functions to dynamically attach attributes to classes.
Most of parsing result is cached because of immutability of input data.
"""


class cached_property(object):
    """
    Copied from Django.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res


def attach_attribute(target, name, attr):
    attr.__name__ = name
    setattr(target, name, attr)


def attach_cached_property(target, name, prop):
    method = cached_property(prop)
    attach_attribute(target, name, method)
