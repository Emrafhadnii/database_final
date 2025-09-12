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


complaints_data_model = Table(
    "complaints",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("driver_id", Integer, ForeignKey("drivers.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("reasons", String(256), nullable=False),
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

class Complaint(AbstractEntity):
    id: int
    driver_id: int
    user_id: int
    reasons: str
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        driver_id: int,
        user_id: int,
        reasons: str,
    ):
        self.driver_id = driver_id
        self.user_id = user_id
        self.reasons = reasons
        self.created_at = datetime.now(UTC)
    
    def update(
        self,
        reasons: str | None = None
    ):
        self.reasons = self.reasons if reasons is None else reasons
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "user_id": self.user_id,
            "reasons": self.reasons,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }
   
    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.COMPLAINT

    @classmethod
    def factory(cls, **kwargs):
        complaint = Complaint(
            driver_id=kwargs["driver_id"],
            user_id=kwargs["user_id"],
            reasons=kwargs["reasons"]
        )
        complaint.id = kwargs["id"]
        complaint.created_at = kwargs["created_at"]
        complaint.updated_at = kwargs.get("updated_at")
        return complaint
