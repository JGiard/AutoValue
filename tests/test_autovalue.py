import pytest

from src.autovalue import autovalue


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
