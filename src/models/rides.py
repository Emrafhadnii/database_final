from sqlalchemy import (
    Column,
    Integer,
    Time,
    String,
    DateTime,
    ForeignKey,
    Table,
    Enum,
    func
)
from config.postgres import mapper_registry
from geoalchemy2 import Geometry
from src.models.enums import RideType, RideStatus, EntityType
from datetime import datetime, UTC, time
from src.shared.abstract_entity import AbstractEntity

rides_data_model = Table(
    "rides",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("driver_id", Integer, ForeignKey("drivers.id")),
    Column("canceller_id", Integer),
    Column("start_address", Geometry(geometry_type='POINT', srid=4326), nullable=False),
    Column("end_address", Geometry(geometry_type='POINT', srid=4326), nullable=False),
    Column("alternative_end_address", Geometry(geometry_type='POINT', srid=4326)),
    Column("stop_time", Time(timezone=False)),
    Column("ride_type", Enum(RideType), nullable=False),
    Column("status", Enum(RideStatus), default=RideStatus.REQUESTED, nullable=False),
    Column("requested_at", DateTime(timezone=True), default=func.now(), nullable=False),
    Column("accepted_at", DateTime(timezone=True)),
    Column("started_at", DateTime(timezone=True)),
    Column("completed_at", DateTime(timezone=True)),
    Column("fare", Integer, nullable=False),
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

class Ride(AbstractEntity):
    id: int
    user_id: int
    driver_id: int | None
    canceller_id: int | None
    start_address: str
    end_address: str
    alternative_end_address: str | None
    stop_time: time | None
    ride_type: RideType
    status: RideStatus
    requested_at: datetime
    accepted_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    fare: int
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        user_id: int,
        start_address: str,
        end_address: str,
        ride_type: RideType,
        fare: int,
        driver_id: int | None = None,
        canceller_id: int | None = None,
        alternative_end_address: str | None = None,
        stop_time: str | None = None,
    ):
        self.user_id = user_id
        self.driver_id = driver_id
        self.canceller_id = canceller_id
        self.start_address = start_address
        self.end_address = end_address
        self.alternative_end_address = alternative_end_address
        self.stop_time = stop_time
        self.ride_type = ride_type
        self.fare = fare
        self.status = RideStatus.REQUESTED
        self.requested_at = datetime.now(UTC)
        # self.created_at = datetime.now(UTC)

    def update_fare(
        self,
        fare: int,
    ):
        if fare is None:
            raise ValueError("Fare cannot be empty")
        self.fare = fare
        self.updated_at = datetime.now(UTC)

    def update_end_address(
        self,
        end_address: int
    ):
        if end_address is None:
            raise ValueError("End address cannot be empty")
        self.end_address = end_address
        self.requested_at = datetime.now(UTC)       
        self.updated_at = datetime.now(UTC)

    def update_start_address(
        self,
        start_address: str
    ):
        if start_address is None:
            raise ValueError("Start address cannot be empty")
        self.start_address = start_address
        self.updated_at = datetime.now(UTC)

    def update_alternative_end_address(
        self,
        alternative_end_address: str
    ):
        if alternative_end_address is None:
            raise ValueError("Alternative end address cannot be empty")
        self.alternative_end_address = alternative_end_address
        self.updated_at = datetime.now(UTC)

    def update_stop_time(
        self,
        stop_time: time
    ):
        if stop_time is None:
            raise ValueError("Stop time cannot be empty")
        self.stop_time = stop_time
        self.updated_at = datetime.now(UTC)

    def cancel_ride(
        self,
        canceller_id: int
    ):
        if canceller_id is None:
            raise ValueError("Canceller ID cannot be empty")
        self.canceller_id = canceller_id
        self.status = RideStatus.CANCELLED
        self.updated_at = datetime.now(UTC)

    def accept_ride(
        self,
        driver_id: int
    ):
        if driver_id is None:
            raise ValueError("Driver ID cannot be empty")
        self.driver_id = driver_id
        self.status = RideStatus.ACCEPTED
        self.accepted_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def ride_completed(self):
        self.status = RideStatus.COMPLETED
        self.completed_at = datetime.now(UTC) 

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "driver_id": self.driver_id,
            "canceller_id": self.canceller_id,
            "start_address": self.start_address,
            "end_address": self.end_address,
            "alternative_end_address": self.alternative_end_address,
            "stop_time": self.stop_time,
            "ride_type": self.ride_type.value,
            "status": self.status.value,
            "requested_at": self.requested_at,
            "accepted_at": self.accepted_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "fare": self.fare,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.RIDE

    @classmethod
    def factory(cls, **kwargs):
        ride = Ride(
            user_id=kwargs["user_id"],
            start_address=kwargs["start_address"],
            end_address=kwargs["end_address"],
            ride_type=RideType.from_value(kwargs["ride_type"]),
            fare=kwargs["fare"],
            driver_id=kwargs.get("driver_id"),
            canceller_id=kwargs.get("canceller_id"),
            alternative_end_address=kwargs.get("alternative_end_address"),
            stop_time=kwargs.get("stop_time"),
        )
        ride.id = kwargs["id"]
        ride.requested_at = kwargs["requested_at"]
        ride.created_at = kwargs["created_at"]
        ride.accepted_at = kwargs.get("accepted_at")
        ride.started_at = kwargs.get("started_at")
        ride.completed_at = kwargs.get("completed_at")
        ride.updated_at = kwargs.get("updated_at")
        ride.status=RideStatus.from_value(kwargs.get("status"))
        return ride
