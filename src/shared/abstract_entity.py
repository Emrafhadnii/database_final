from abc import ABC, abstractmethod
from ..models.enums import EntityType
from datetime import datetime, timedelta
from enum import Enum

def convert_value(type_, value):
    if not value:
        return value
    if type_ == datetime:
        return datetime.fromisoformat(value) if isinstance(value, str) else value
    elif type_ == int:
        return int(value)
    elif type_ == float:
        return float(value)
    elif type_ == str:
        return str(value)
    elif type_ == timedelta:
        parts = [int(part) for part in value.split(":")]
        return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
    elif isinstance(type_, type) and issubclass(type_, Enum) and hasattr(type_, "from_name"):
        return type_.from_name(value)
    else:
        return value


class AbstractEntity(ABC):
    def to_dict(self, **kwargs) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    @abstractmethod
    def entity_type(cls) -> EntityType: ...


    @classmethod
    def factory(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            if key in cls.__annotations__:
                setattr(instance, key, convert_value(cls.__annotations__[key], value))
        return instance

