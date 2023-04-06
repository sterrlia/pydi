from typing import Type, Union
from abc import ABC, abstractmethod


class AbstractContainer(ABC):
    @abstractmethod
    def get_service(self, ref) -> Union[object, None]:
        raise NotImplementedError

    @abstractmethod
    def set_service(self, ref, service: object):
        raise NotImplementedError

    @abstractmethod
    def get(self, ref) -> object:
        raise NotImplementedError

    @abstractmethod
    def get_parameter(self, name: str) -> Union[str, int, float, None]:
        raise NotImplementedError

    @abstractmethod
    def has_service(self, ref: Union[Type, str]) -> bool:
        raise NotImplementedError

