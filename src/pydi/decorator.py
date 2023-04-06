def interface(object):
    object.__abstractmethods__ = True
    return object

