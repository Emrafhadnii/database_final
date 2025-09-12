from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Table,
    func
)
from config.postgres import mapper_registry
from src.models.enums import VehicleType, EntityType
from src.shared.abstract_entity import AbstractEntity
from datetime import datetime, UTC


vehicles_data_model = Table(
    "vehicles",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True), 
    Column("owner_id", Integer, ForeignKey("drivers.id"), nullable=False),
    Column("model", String(50), nullable=False),
    Column("year", Integer, nullable=False),
    Column("license_plate", String(20), unique=True, nullable=False),
    Column("vehicle_type", Enum(VehicleType), nullable=False),
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

class Vehicle(AbstractEntity):
    id: int
    owner_id: int
    model: str
    year: int
    license_plate: str
    vehicle_type: VehicleType
    created_at: datetime 
    updated_at: datetime | None

    def __init__(
        self,
        owner_id: int,
        model: str,
        year: int,
        license_plate: str,
        vehicle_type: VehicleType,
    ):
        self.owner_id = owner_id
        self.model = model
        self.year = year
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.created_at = datetime.now(UTC)
    

    def update(
        self,
        owner_id: int | None = None
    ):
        self.owner_id = self.owner_id if owner_id is None else owner_id
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "model": self.model,
            "year": self.year,
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }
    
    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.VEHICLE

    @classmethod
    def factory(cls, **kwargs):
        vehicle = Vehicle(
            owner_id=kwargs["owner_id"],
            model=kwargs["model"],
            year=kwargs["year"],
            license_plate=kwargs["license_plate"],
            vehicle_type=VehicleType.from_value(kwargs["vehicle_type"])
        )
        vehicle.id = kwargs["id"]
        vehicle.created_at = kwargs["created_at"]
        vehicle.updated_at = kwargs.get("updated_at")
        return vehicle

