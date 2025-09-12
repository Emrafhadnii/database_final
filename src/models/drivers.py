from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Table,
    func,
    UniqueConstraint,
    String
)

from config.postgres import mapper_registry
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity
from .enums import EntityType


drivers_data_model = Table(
    "drivers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("na_code", Integer, unique=True, nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
    Column("ce_code", Integer, unique=True, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now()
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        onupdate=func.now(),
        default=func.now()
    ),
)

class Driver(AbstractEntity):
    id: int
    na_code: int
    first_name: str
    last_name: str
    ce_code: int
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        na_code: int,
        first_name: str,
        last_name: str,
        ce_code: int,
    ):
        self.na_code = na_code
        self.first_name = first_name
        self.last_name = last_name
        self.ce_code = ce_code
        self.created_at = datetime.now(UTC)
    
    def update(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        self.first_name = self.first_name if first_name is None else first_name
        self.last_name = self.last_name if last_name is None else last_name
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "na_code": self.na_code,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "ce_code": self.ce_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.DRIVER

    @classmethod
    def factory(cls, **kwargs):
        driver = Driver(
            na_code=kwargs["na_code"],
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            ce_code=kwargs["ce_code"]
        )
        driver.id = kwargs["id"]
        driver.created_at = kwargs["created_at"]
        driver.updated_at = kwargs.get("updated_at")
        return driver
