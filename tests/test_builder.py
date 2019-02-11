from autovalue import autovalue


def test_basic():
    @autovalue
    class Foo:
        def __init__(self, a: int, b: int, c: int):
            self.a = a
            self.b = b
            self.c = c

    foo = Foo(1, 2, 3).update(a=4)
    assert foo.a == 4
    assert foo.b == 2
    assert foo.c == 3


def test_update_should_not_modify_object():
    @autovalue
    class Foo:
        def __init__(self, a: int, b: int, c: int):
            self.a = a
            self.b = b
            self.c = c

    foo1 = Foo(1, 2, 3)
    foo2 = foo1.update(a=4)

    assert foo2.a == 4
    assert foo1.a == 1
