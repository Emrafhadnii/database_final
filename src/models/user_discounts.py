from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    func
)
from config.postgres import mapper_registry
from src.shared.abstract_entity import AbstractEntity
from .enums import EntityType
from datetime import datetime

user_discounts_data_model = Table(
    "user_discounts",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("discount_id", Integer, ForeignKey("discounts.id"), nullable=False),
    Column("used", Boolean, default=False, nullable=False),
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

class UserDiscount(AbstractEntity):
    id: int
    user_id: int
    discount_id: int
    used: bool
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        user_id: int,
        discount_id: int,
    ):
        self.user_id = user_id
        self.discount_id = discount_id
        self.used = False

    def use(self):
        self.used = True

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "discount_id": self.discount_id,
            "used": self.used,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.USER_DISCOUNT

    @classmethod
    def factory(cls, **kwargs):
        user_discount = UserDiscount(
            user_id=kwargs["user_id"],
            discount_id=kwargs["discount_id"],
        )
        user_discount.id = kwargs["id"]
        user_discount.used = kwargs["used"]
        user_discount.created_at = kwargs["created_at"]
        user_discount.updated_at = kwargs["updated_at"]
        return user_discount
