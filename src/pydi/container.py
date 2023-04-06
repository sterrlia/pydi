from .error import ContainerException
from .abstract import AbstractContainer
from .config import Config, BuildScheme
from . import util
from typing import List, Tuple, Union, Type, Dict


class Container(AbstractContainer):
    def __init__(
        self,
        config: Union[Config, dict] = dict(),
        build_schemes: Union[List[BuildScheme], Tuple[BuildScheme]] = [],
    ) -> None:
        self.config: dict = config if util.is_same_type(config, dict) else config.dict()  # type: ignore

        scheme_map = {}
        for scheme in build_schemes:
            ref = scheme.getRef()
            name = scheme.getName()
            scheme_map[name if name else ref] = scheme

        self.build_schemes = scheme_map
        self.services: Dict[Union[Type, str], object] = {}

        super().__init__()

    def get(self, ref: Union[Type, str]) -> object:
        if util.is_class(ref) or util.is_typed_list(ref):
            service = self.construct(ref, self.get_build_scheme(ref=ref))
            return service
        elif type(ref) is str:
            service = self.get_service(ref)
            if service is None:
                return self.get_parameter(ref)

            return service
        else:
            raise ContainerException(f"Invalid classname {ref}")

    def get_service(self, ref: Union[Type, str]) -> Union[object, None]:
        if ref in self.services.keys():
            return self.services[ref]
        else:
            return None

    def get_build_scheme(
        self, name: Union[str, None] = None, ref: Union[Type, None] = None
    ) -> Union[BuildScheme, None]:
        if name in self.build_schemes.keys():
            scheme = self.build_schemes[name]
        elif ref in self.build_schemes.keys():
            scheme = self.build_schemes[ref]
        else:
            for key, scheme in self.build_schemes.items():
                if scheme.getRef() == ref:
                    return scheme

            return None

        if scheme.getRef() == ref:
            return scheme
        else:
            raise ContainerException(
                f"Service '{util.get_name(ref)}' uses wrong build scheme"
            )

    def get_parameter(self, name: str) -> Union[str, int, float]:
        if name in self.config.keys():
            return self.config[name]

        raise ContainerException(f"Unknown parameter '{name}'")

    def set_service(self, key: str, service: object):
        if util.is_abstract(service):
            raise ContainerException(
                f"Service '{util.get_name(service)}' is abstract class"
            )

        if key in self.services.keys():
            raise ContainerException(f"Service with key '{key}' already loaded")

        self.services[key] = service

    def has_service(self, ref: Union[Type, str]) -> bool:
        return ref in self.services.keys()

    def get_service_list(self, list_ref: Type) -> List:
        item_ref = util.get_list_item_type(list_ref)
        if util.is_abstract(item_ref):
            result = list()
            for subclass in util.get_subclasses(item_ref):
                if util.is_abstract(subclass):
                    continue

                result.append(self.construct(subclass))

            return result

        raise ContainerException("List item class is not abstract")

    def resolve_argument(self, name: str, annotation: Type):
        if self.has_service(name):
            service = self.get_service(name)
            if util.is_same_type(service, annotation) or util.is_subclass(
                service, annotation
            ):
                return service
        elif util.is_primitive_type(annotation):
            parameter = self.get_parameter(name)

            if not util.is_same_type(annotation, parameter):
                raise ContainerException(
                    f"Wrong parameter type '{util.get_name(parameter)}'"
                )

            return parameter
        else:
            build_scheme = self.get_build_scheme(name=name, ref=annotation)
            return self.construct(annotation, build_scheme)

    def construct(
        self, ref: Type, scheme: Union[BuildScheme, None] = None
    ) -> Union[object, List]:
        if util.is_typed_list(ref):
            return self.get_service_list(ref)

        while util.is_abstract(ref):
            subclasses = util.get_subclasses(ref)
            if subclasses:
                ref = subclasses[0]
            else:
                raise ContainerException(
                    "No implementation found for " + util.get_name(ref)
                )

        if self.has_service(ref):
            return self.get_service(ref)

        arguments_data = util.get_constructor_arguments(ref)
        if not arguments_data:
            service = ref()
            self.set_service(ref, service)
            return service

        scheme_arguments: dict = {} if scheme is None else scheme.getArgs()

        arguments = {}
        for name, annotation in arguments_data.items():
            if name in scheme_arguments.keys():
                scheme_arg = scheme_arguments[name]
            elif annotation in scheme_arguments.keys():
                scheme_arg = scheme_arguments[annotation]
            else:
                scheme_arg = None

            if scheme_arg is BuildScheme:
                value = self.construct(annotation, scheme_arg)
            elif not scheme_arg is None:
                value = scheme_arg
            else:
                value = self.resolve_argument(name, annotation)

            arguments[name] = value

        service = ref(**arguments)
        self.set_service(ref, service)
        return service
