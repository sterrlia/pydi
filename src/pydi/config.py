from typing import Any, Dict, List, Type, Union

class BuildScheme:
    def __init__(self, ref: Type, args: dict, name: Union[str, None] = None) -> None:
        self.name = name
        self.ref = ref
        self.args = args

    def getName(self) -> Union[str, None]:
        return self.name

    def getRef(self) -> Type:
        return self.ref

    def getArgs(self) -> Dict[str, Any]:
        return self.args

class Config:
    def __init__(self, data: dict):
        self.__dict__.update(data)

    def has_key(self, key) -> bool:
        return key in self.__dict__.keys()

    def dict(self) -> dict:
        return self.__dict__

class AbstractConfigProvider:
    def get_config(self) -> Config:
        raise NotImplementedError

class AbstractBuildSchemeProvider:
    def get_schemes(self) -> List[BuildScheme]:
        raise NotImplementedError
