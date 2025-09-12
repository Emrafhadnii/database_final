from enum import Enum
from typing import TypeVar,Type


T = TypeVar("T", bound="BaseEnum")


class BaseEnum(Enum):
    @classmethod
    def from_value(cls: Type[T], value: str | int) -> T:
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Value {value} not found in {cls.__name__}")

    @classmethod
    def from_name(cls: Type[T], name: str) -> T:
        try:
            return cls[name]
        except KeyError:
            raise KeyError(f"Name {name} not found in {cls.__name__}")

    @classmethod
    def has_name(cls, name: str) -> bool:
        return name in cls.__members__
