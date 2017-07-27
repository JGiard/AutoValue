from functools import wraps
from inspect import getmembers, signature

__version__ = '0.4'


def autovalue(cls):
    attributes = []
    for member in getmembers(cls):
        if member[0] == '__init__':
            for name, parameter in signature(member[1]).parameters.items():
                if name != 'self':
                    attributes.append(name)

    def init(self, *args, **kwargs):
        cls.__init__(self, *args, **kwargs)
        self.__initialized = True

    def setter(self, key, value):
        if self.__initialized and key in attributes:
            raise ValueError('cannot assign member {} to class {}'.format(key, cls.__name__))
        cls.__setattr__(self, key, value)

    def eq(self, other):
        if type(self) != type(other):
            return False
        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def tostring(self):
        attr_format = ['{}={}'.format(name, str(getattr(self, name))) for name in attributes]
        return '{}({})'.format(cls.__name__, ', '.join(attr_format))

    wraps(cls.__init__)(init)

    methods = {'__init__': init,
               '__setattr__': setter,
               '__initialized': False}

    if cls.__str__ == object.__str__:
        methods['__str__'] = tostring
    if cls.__repr__ == object.__repr__:
        methods['__repr__'] = tostring
    if cls.__eq__ == object.__eq__:
        methods['__eq__'] = eq

    name = 'AutoValue_{}'.format(cls.__name__)
    auto_value = type(name, (cls,), methods)

    return auto_value
