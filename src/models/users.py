from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    Enum,
    func
)
from config.postgres import mapper_registry
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity
from .enums import EntityType


users_data_model = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("phone", String(20), unique=True, nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
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
    )
)

class User(AbstractEntity):
    id: int
    phone: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        phone: str,
        first_name: str,
        last_name: str,
    ):
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        # self.created_at = datetime.now(UTC)
    
    def update(
        self,
        phone: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
    ):
        self.phone = self.phone if phone is None else phone
        self.first_name = self.first_name if first_name is None else first_name
        self.last_name = self.last_name if last_name is None else last_name
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.USER

    @classmethod
    def factory(cls, **kwargs):
        user = User(
            phone=kwargs["phone"],
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"]
        )
        user.id = kwargs["id"]
        user.created_at = kwargs["created_at"]
        user.updated_at = kwargs["updated_at"]
        return user
