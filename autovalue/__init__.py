from collections.abc import Hashable
from functools import wraps
from inspect import getmembers, signature

__version__ = '0.7.3'


def autovalue(cls):
    attributes = []
    for member in getmembers(cls):
        if member[0] == '__init__':
            for name, parameter in signature(member[1]).parameters.items():
                if name != 'self':
                    attributes.append(name)

    old_init = cls.__init__

    def init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        self.__initialized = True

    def setter(self, key, value):
        if self.__initialized and key in attributes:
            raise ValueError('cannot assign member {} to class {}'.format(key, cls.__name__))
        super(cls, self).__setattr__(key, value)

    def eq(self, other):
        if type(self) != type(other):
            return False
        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def cls_hash(self):
        values = []
        for attr in attributes:
            value = getattr(self, attr)
            if not isinstance(value, Hashable):
                if isinstance(value, list):
                    values.append(tuple(value))
                elif isinstance(value, dict):
                    values.append(tuple(value.items()))
                else:
                    raise TypeError('unhashable type: \'{}\''.format(type(value)))
            else:
                values.append(value)
        return hash(tuple(values))

    def tostring(self):
        attr_format = ['{}={}'.format(name, str(getattr(self, name))) for name in attributes]
        return '{}({})'.format(cls.__name__, ', '.join(attr_format))

    def update(self, **kwargs) -> cls:
        cls_args = {attr: getattr(self, attr) for attr in attributes}
        for k, v in kwargs.items():
            cls_args[k] = v
        return cls(**cls_args)

    wraps(cls.__init__)(init)

    setattr(cls, '__init__', init)
    setattr(cls, '__initialized', False)
    if not hasattr(cls, 'update'):
        setattr(cls, 'update', update)
    if cls.__str__ == object.__str__:
        setattr(cls, '__str__', tostring)
    if cls.__repr__ == object.__repr__:
        setattr(cls, '__repr__', tostring)
    if cls.__eq__ == object.__eq__:
        setattr(cls, '__eq__', eq)
        setattr(cls, '__hash__', cls_hash)
    setattr(cls, '__setattr__', setter)

    return cls
