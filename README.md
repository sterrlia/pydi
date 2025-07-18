## DI container for python

- I wrote this a long time ago

### Usage
```python
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

    scheme = BuildScheme(SubClass, dict(param=param))

    container = Container(build_schemes=[scheme])
    instance: Class = container.get(Class) # type: ignore
```
