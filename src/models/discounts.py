from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    CheckConstraint,
    Table,
    Enum,
    func
)
from config.postgres import mapper_registry
from src.models.enums import DiscountType , EntityType
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity

discounts_data_model = Table(
    "discounts",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("expire_time", DateTime(timezone=True), nullable=False),
    Column("code", String(16), unique=True, nullable=False),
    Column("percentage", Numeric(2,2)),  
    Column("amount", Integer),
    Column(
        "ride_type", 
        Enum(DiscountType), 
        default=DiscountType.ALL  
    ),
    Column(
        "created_at", 
        DateTime(timezone=True), 
        default=func.now()
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        onupdate=func.now(),
        default=func.now()
    ),
    CheckConstraint(
        "(percentage IS NOT NULL AND amount IS NULL) OR "
        "(percentage IS NULL AND amount IS NOT NULL)",
        name="valid_discount"
    )
)

class Discount(AbstractEntity):
    id: int
    expire_time: datetime
    code: str
    percentage: float | None
    amount: int | None
    ride_type: DiscountType | None
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        expire_time: datetime,
        code: str,
        percentage: float | None = None,
        amount: int | None = None,
        ride_type: DiscountType | None = DiscountType.ALL
    ):
        if not percentage is None and amount is None:
            raise ValueError("Discount must have either percentage or amount, but not both")
            
        self.expire_time = expire_time
        self.code = code
        self.percentage = percentage
        self.amount = amount
        self.ride_type = ride_type
        self.created_at = datetime.now(UTC)

    def update(
        self,
        expire_time: datetime | None = None,
        percentage: float | None = None,
        amount: int | None = None,
        ride_type: DiscountType | None = None
    ):
        if percentage is not None and amount is not None:
            raise ValueError("Cannot set both percentage and amount")
            
        self.expire_time = self.expire_time if expire_time is None else expire_time
        self.percentage = self.percentage if percentage is None else percentage
        self.amount = self.amount if amount is None else amount
        self.ride_type = self.ride_type if ride_type is None else ride_type
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "expire_time": self.expire_time,
            "code": self.code,
            "percentage": self.percentage, 
            "amount": self.amount,
            "ride_type": self.ride_type.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.DISCOUNT

    @classmethod
    def factory(cls, **kwargs):
        discount = Discount(
            expire_time=kwargs["expire_time"],
            code=kwargs["code"],
            percentage=kwargs.get("percentage"),
            amount=kwargs.get("amount"),
            ride_type=DiscountType.from_value(kwargs["ride_type"]) if kwargs.get("ride_type") else None
        )
        discount.id = kwargs["id"]
        discount.created_at = kwargs["created_at"]
        discount.updated_at = kwargs.get("updated_at")
        return discount
