from os import walk
from abc import ABC
from typing import Dict, Generic, List, Tuple, Type, Union, get_origin
import inspect


def get_name(object: Union[Type, object]) -> str:
    ref = get_ref(object)
    return ref.__name__

def get_subclasses(object: Union[Type, object]) -> List[object]:
    return list(get_ref(object).__subclasses__())


def is_primitive_type(data) -> bool:
    return get_ref(data) in [str, int, float]


def is_instance(data) -> bool:
    return not is_type(data) and is_class(data)


def is_class(data) -> bool:
    return type(data) == type


def is_type(data) -> bool:
    return data is str or data is int or data is float or get_origin(data) in [
        Union,
        Type,
        List,
        Dict,
        Generic,
        Tuple,
        list,
        dict,
        str,
        float,
        int,
    ]


def is_subclass(sub: Union[Type, object], parent: Union[Type, object]) -> bool:
    return issubclass(get_ref(sub), get_ref(parent))


def get_constructor_arguments(object: Union[Type, object]) -> Dict[str, Type]:
    result = {}
    for name, data in inspect.signature(object.__init__).parameters.items():
        if name == "self":
            continue

        if name == "args" or name == "kwargs":
            return {}

        result[data.name] = get_ref(data.annotation)

    return result


def is_abstract(object: Union[Type, object]) -> bool:
    return inspect.isabstract(object)


def is_list(object: Union[Type, object]) -> bool:
    return get_origin(object) in [list, List]


def is_same_type(first: Union[Type, object], second: Union[Type, object]) -> bool:
    return get_ref(first) == get_ref(second)


def is_typed_list(object: Union[Type, object]) -> bool:
    ref = get_ref(object)

    return (
        is_list(object)
        and hasattr(ref, "__args__")
        and hasattr(ref, "_name")
        and ref._name == "List"
    )


def get_list_item_type(object: Union[List, Type]) -> Type:
    ref = get_ref(object)
    return ref.__args__[0]


def get_ref(object: Union[Type, object]) -> Type:
    ref: Type = object if is_class(object) or is_type(object) else object.__class__

    return ref

