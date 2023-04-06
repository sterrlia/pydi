from typing import List
import unittest
from pydi.config import BuildScheme
from pydi.container import Container
from pydi.decorator import interface

class SubClass:
    def __init__(self, param: str) -> None:
        self.param = param

    def get_param(self) -> str:
        return self.param

class Class:
    def __init__(self, sub: SubClass) -> None:
        self.sub = sub

    def get_sub(self) -> SubClass:
        return self.sub


class TestContainer(unittest.TestCase):
    class Empty:
        ...

    def test_get_empty_class(self):
        container = Container()
        expected = self.Empty()
        actual = container.get(self.Empty)
        self.assertEqual(expected.__class__, actual.__class__)

    def test_get_parameter(self):
        config = dict(param1=3, param2=4, ppp=5)

        container = Container(config=config)

        for key, value in config.items():
            container_value = container.get(key)
            self.assertEqual(container_value, value)

    class WithParameter:
        def __init__(self, param: str):
            self.param = param

        def getParam(self) -> str:
            return self.param

    def test_with_parameter(self):
        config = dict(param="heck")
        container = Container(config=config)

        instance: WithParameter = container.get(self.WithParameter)  # type: ignore

        self.assertEqual(instance.getParam(), config["param"])

    @interface
    class Abstraction:
        ...

    class Realization(Abstraction):
        ...

    def test_with_abstract_class(self):
        container = Container()

        instance = container.get(self.Abstraction)

        self.assertEqual(instance.__class__, self.Realization)

    @interface
    class AbstractionForList:
        ...

    class RealizationForList1(AbstractionForList):
        ...

    class RealizationForList2(AbstractionForList):
        ...

    def test_get_list(self):
        container = Container()
        
        instances: List = container.get(List[self.AbstractionForList])  # type: ignore

        self.assertEqual(self.RealizationForList1, instances[0].__class__)
        self.assertEqual(self.RealizationForList2, instances[1].__class__)


    def test_with_build_scheme(self):
        param = "striiiing"
        scheme = BuildScheme(SubClass, dict(param=param))

        container = Container(build_schemes=dict(service=scheme))
        instance: Class = container.get(Class) # type: ignore

        self.assertEqual(instance.get_sub().get_param(), param)
