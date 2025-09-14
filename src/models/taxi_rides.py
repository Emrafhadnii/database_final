from sqlalchemy import (
    Column,
    Integer,
    Time,
    ForeignKey,
    Table,
    DateTime,
    func
)
from config.postgres import mapper_registry
from src.models.enums import EntityType
from src.shared.abstract_entity import AbstractEntity
from geoalchemy2 import Geometry
from datetime import time, datetime


taxi_rides_data_model = Table(
    "taxi_rides",
    mapper_registry.metadata,
    Column("ride_id", Integer, ForeignKey("rides.id"), primary_key=True),
    Column("alternative_end_address", Geometry(geometry_type='POINT', srid=4326)),
    Column("stop_time", Time(timezone=False)),
)


class TaxiRide(AbstractEntity):
    ride_id: int
    alternative_end_address: str | None
    stop_time: time | None

    def __init__(
        self,
        ride_id: int,
        alternative_end_address: str | None = None,
        stop_time: time | None = None,
    ):
        self.ride_id = ride_id
        self.alternative_end_address = alternative_end_address
        self.stop_time = stop_time

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.TAXI_RIDE

    def to_dict(self, **kwargs) -> dict:
        return {
            "ride_id": self.ride_id,
            "alternative_end_address": self.alternative_end_address,
            "stop_time": self.stop_time,
            **kwargs,
        }

    @classmethod
    def factory(cls, **kwargs):
        return cls(
            ride_id=kwargs["ride_id"],
            alternative_end_address=kwargs.get("alternative_end_address"),
            stop_time=kwargs.get("stop_time"),
        )
