from typing import Dict, Optional, Type

from .base import BasePerson
from .student import Student
from .starosta import Starosta
from .proforg import Proforg

TYPE_REGISTRY: Dict[str, Type[BasePerson]] = {
    "Student": Student,
    "Starosta": Starosta,
    "Proforg": Proforg,
}


def get_type(name: str) -> Optional[Type[BasePerson]]:
    return TYPE_REGISTRY.get(name)


def list_type_names():
    return list(TYPE_REGISTRY.keys())

