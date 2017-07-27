from inspect import getmembers, signature

__version__ = '0.1'


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
        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def tostring(self):
        attr_format = ['{}={}'.format(name, str(getattr(self, name))) for name in attributes]
        return '{}({})'.format(cls.__name__, ', '.join(attr_format))

    name = 'AutoValue_{}'.format(cls.__name__)
    auto_value = type(name, (cls,),
                      {'__init__': init,
                       '__setattr__': setter,
                       '__eq__': eq,
                       '__str__': tostring,
                       '__repr__': tostring,
                       '__initialized': False})

    return auto_value
