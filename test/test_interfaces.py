# coding: utf-8
from pyanyapi.interfaces import IndexOfInterface


def test_indexof_interface():
    interface = IndexOfInterface('this is dummy content')
    assert interface.parse('dummy')
    assert not interface.parse('foo')
