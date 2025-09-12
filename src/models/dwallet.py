from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    func
)
from config.postgres import mapper_registry
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity
from .enums import EntityType

dwallet_data_model = Table(
    "dwallet",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True), 
    Column("driver_id", Integer, ForeignKey("drivers.id"), nullable=False),
    Column("bank_account", String(16), unique=True, nullable=False),
    Column("balance", Integer, default=0),
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

class DWallet(AbstractEntity):
    id: int
    driver_id: int
    bank_account: str
    balance: int | None = 0
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        driver_id: int,
        bank_account: str,
        balance: int | None = 0
    ):
        self.driver_id = driver_id
        self.bank_account = bank_account
        self.balance = balance if balance else 0
        self.created_at = datetime.now(UTC)
    
    def update(
        self,
        bank_account: str | None = None,
    ):
        self.bank_account = self.bank_account if bank_account is None else bank_account
        self.updated_at = datetime.now(UTC)

    def add_balance(self, amount: int):
        self.balance += amount
        self.updated_at = datetime.now(UTC)

    def deduct_balance(self, amount: int):
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "bank_account": self.bank_account,
            "balance": self.balance,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.DWALLET

    @classmethod
    def factory(cls, **kwargs):
        dwallet = DWallet(
            driver_id=kwargs["driver_id"],
            bank_account=kwargs["bank_account"],
            balance=kwargs.get("balance", 0)
        )
        dwallet.id = kwargs["id"]
        dwallet.created_at = kwargs["created_at"]
        dwallet.updated_at = kwargs.get("updated_at")
        return dwallet
