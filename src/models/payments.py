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
from src.models.enums import PaymentMethod, EntityType
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity

payments_data_model = Table(
    "payments",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("ride_id", Integer, ForeignKey("rides.id"), nullable=False),
    Column("amount", Integer, nullable=False),
    Column("payment_method", Enum(PaymentMethod), default=PaymentMethod.CASH, nullable=False),
    Column("transaction_id", String(100), unique=True, nullable=False),
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

class Payment(AbstractEntity):
    id: int
    user_id: int
    ride_id: int
    amount: int
    payment_method: PaymentMethod
    transaction_id: str
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        user_id: int,
        ride_id: int,
        amount: int,
        payment_method: PaymentMethod = PaymentMethod.CASH,
        transaction_id: str | None = None
    ):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
            
        self.user_id = user_id
        self.ride_id = ride_id
        self.amount = amount
        self.payment_method = payment_method
        self.transaction_id = transaction_id
        self.created_at = datetime.now(UTC)

    def update(
        self,
        amount: int | None = None,
        payment_method: PaymentMethod | None = None,
    ):
        if amount is not None and amount <= 0:
            raise ValueError("Payment amount must be positive")
            
        self.amount = self.amount if amount is None else amount
        self.payment_method = self.payment_method if payment_method is None else payment_method
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ride_id": self.ride_id,
            "amount": self.amount,
            "payment_method": self.payment_method.value,  
            "transaction_id": self.transaction_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.PAYMENT

    @classmethod
    def factory(cls, **kwargs):
        payment = Payment(
            user_id=kwargs["user_id"],
            ride_id=kwargs["ride_id"],
            amount=kwargs["amount"],
            payment_method=PaymentMethod.from_value(kwargs["payment_method"]),
            transaction_id=kwargs.get("transaction_id")
        )
        payment.id = kwargs["id"]
        payment.created_at = kwargs["created_at"]
        payment.updated_at = kwargs.get("updated_at")
        return payment
