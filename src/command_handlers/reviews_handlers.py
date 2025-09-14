from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.reviews import Review
from fastapi import HTTPException
from src.endpoints.dependencies.redis_dependency import redis_dependency
import json


@dataclass
class CreateReview:
    ride_id: int
    user_id: int
    driver_id: int
    rating: int
    comment: str | None = None


@dataclass
class UpdateReview:
    id: int
    rating: int | None = None
    comment: str | None = None


@dataclass
class DeleteReview:
    id: int


from src.endpoints.dependencies.bus_dependency import messagebus
from src.events import ReviewCreated


async def handle_create_review(command: CreateReview, uow: UnitOfWork):
    async with uow:
        review = Review(
            ride_id=command.ride_id,
            user_id=command.user_id,
            driver_id=command.driver_id,
            rating=command.rating,
            comment=command.comment,
        )

        await uow.review.insert(review)

        event = ReviewCreated(
            id=review.id,
            ride_id=review.ride_id,
            user_id=review.user_id,
            driver_id=review.driver_id,
            rating=review.rating,
            comment=review.comment,
        )
        await messagebus.publish(
            "review_created",
            event.dict()
        )


async def handle_update_review(command: UpdateReview, uow: UnitOfWork):
    async with uow:
        review = await uow.review.select_by_id(Review, command.id)
        if not review:
            raise HTTPException(404, "entity not found")
        review.update(
            rating=command.rating,
            comment=command.comment,
        )
        await uow.review.update(review)
        await redis_dependency.set(f"{Review.entity_type()}:{command.id}", json.dumps(review.to_dict()), ex=3600)


async def handle_delete_review(command: DeleteReview, uow: UnitOfWork):
    async with uow:
        review = await uow.review.select_by_id(Review, command.id)
        if not review:
            raise HTTPException(404, "entity not found")
        await uow.review.delete(review)
        await redis_dependency.delete(f"{Review.entity_type()}:{command.id}")
