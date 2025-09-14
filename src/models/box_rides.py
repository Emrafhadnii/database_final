from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Table,
    DateTime,
    func
)
from config.postgres import mapper_registry
from src.models.enums import BoxInsurance, ConsignmentType, EntityType
from src.shared.abstract_entity import AbstractEntity
from datetime import datetime


box_rides_data_model = Table(
    "box_rides",
    mapper_registry.metadata,
    Column("ride_id", Integer, ForeignKey("rides.id"), primary_key=True),
    Column("sender_name", String(255), nullable=False),
    Column("sender_phone", String(20), nullable=False),
    Column("recipient_name", String(255), nullable=False),
    Column("recipient_phone", String(20), nullable=False),
    Column("max_insurance", Enum(BoxInsurance), nullable=False),
    Column("consignment_type", Enum(ConsignmentType), nullable=False),
)


class BoxRide(AbstractEntity):
    ride_id: int
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    max_insurance: BoxInsurance
    consignment_type: ConsignmentType

    def __init__(
        self,
        ride_id: int,
        sender_name: str,
        sender_phone: str,
        recipient_name: str,
        recipient_phone: str,
        max_insurance: BoxInsurance,
        consignment_type: ConsignmentType,
    ):
        self.ride_id = ride_id
        self.sender_name = sender_name
        self.sender_phone = sender_phone
        self.recipient_name = recipient_name
        self.recipient_phone = recipient_phone
        self.max_insurance = max_insurance
        self.consignment_type = consignment_type

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.BOX_RIDE

    def to_dict(self, **kwargs) -> dict:
        return {
            "ride_id": self.ride_id,
            "sender_name": self.sender_name,
            "sender_phone": self.sender_phone,
            "recipient_name": self.recipient_name,
            "recipient_phone": self.recipient_phone,
            "max_insurance": self.max_insurance.value,
            "consignment_type": self.consignment_type.value,
            **kwargs,
        }

    @classmethod
    def factory(cls, **kwargs):
        return cls(
            ride_id=kwargs["ride_id"],
            sender_name=kwargs["sender_name"],
            sender_phone=kwargs["sender_phone"],
            recipient_name=kwargs["recipient_name"],
            recipient_phone=kwargs["recipient_phone"],
            max_insurance=BoxInsurance.from_value(kwargs["max_insurance"]),
            consignment_type=ConsignmentType.from_value(kwargs["consignment_type"]),
        )
