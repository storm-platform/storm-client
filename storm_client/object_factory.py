
class ObjectFactory:

    _factories = {}

    @classmethod
    def register(cls, name, factory):
        cls._factories[name] = factory

    @classmethod
    def exists(cls, name):
        return name in cls._factories

    @classmethod
    def resolve(cls, datatype, data):
        return cls._factories[datatype](data)
