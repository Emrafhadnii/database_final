from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Table,
    Enum,
    CheckConstraint,
    func
)
from config.postgres import mapper_registry
from datetime import datetime, UTC
from src.shared.abstract_entity import AbstractEntity
from .enums import EntityType

reviews_data_model = Table(
    "reviews",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ride_id", Integer, ForeignKey("rides.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("driver_id", Integer, ForeignKey("drivers.id"), nullable=False),
    Column("rating", Integer, nullable=False),
    Column("comment", Text),
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
    ),
    CheckConstraint("rating >= 1 AND rating <= 5", name="valid_rating")
)

class Review(AbstractEntity):
    id: int
    ride_id: int
    user_id: int
    driver_id: int
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime | None

    def __init__(
        self,
        ride_id: int,
        user_id: int,
        driver_id: int,
        rating: int,
        comment: str | None = None
    ):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        self.ride_id = ride_id
        self.user_id = user_id
        self.driver_id = driver_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.now(UTC)

    def update(
        self,
        rating: int | None = None,
        comment: str | None = None
    ):
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        self.rating = self.rating if rating is None else rating
        self.comment = self.comment if comment is None else comment
        self.updated_at = datetime.now(UTC)

    def to_dict(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "ride_id": self.ride_id,
            "user_id": self.user_id,
            "driver_id": self.driver_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **kwargs
        }
    
    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.REVIEW

    @classmethod
    def factory(cls, **kwargs):
        review = Review(
            ride_id=kwargs["ride_id"],
            user_id=kwargs["user_id"],
            driver_id=kwargs["driver_id"],
            rating=kwargs["rating"],
            comment=kwargs.get("comment")
        )
        review.id = kwargs["id"]
        review.created_at = kwargs["created_at"]
        review.updated_at = kwargs.get("updated_at")
        return review
