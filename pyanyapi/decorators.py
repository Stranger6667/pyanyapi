# coding: utf-8


def interface_property(method):
    """
    Marks method to be included in parsing result as property.
    """
    method._interface_property = True
    return staticmethod(method)


def interface_method(method):
    """
    Marks method to be included in parsing result.
    """
    method._interface_method = True
    return staticmethod(method)
