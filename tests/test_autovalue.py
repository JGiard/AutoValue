from inspect import signature

import pytest

from autovalue import autovalue


def test_cannot_set_attribute():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    foo = Foo('bar')

    with pytest.raises(ValueError):
        foo.bar = 'bar2'


def test_tostring():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    foo = Foo('bar')

    assert str(foo) == 'Foo(bar=bar)'


def test_equal():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    assert Foo('bar') == Foo('bar')
    assert Foo('bar') != Foo('bar2')


def test_preserve_signature():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    parameters = list(signature(Foo.__init__).parameters.values())
    assert len(parameters) == 2
    assert parameters[1].name == 'bar'
    assert parameters[1].annotation == str


def test_custom_tostring():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

        def __str__(self):
            return '42'

    assert str(Foo('bar')) == '42'


def test_compare_none():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    assert Foo('foo') != None


def test_compare_different_class():
    @autovalue
    class Foo:
        def __init__(self, bar: str):
            self.bar = bar

    @autovalue
    class Quz:
        def __init__(self, bar: str):
            self.bar = bar

    assert Foo('foo') != Quz('foo')
