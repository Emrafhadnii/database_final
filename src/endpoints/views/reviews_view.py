from src.service_layer.unit_of_work import UnitOfWork
from src.models.reviews import Review
from typing import List
from config.mongo_db import db


async def get_all_reviews(uow: UnitOfWork):
    async with uow:
        reviews = await uow.review.select_all(Review)
        return [review.to_dict() for review in reviews]


async def get_review_by_id(review_id: int, uow: UnitOfWork):
    async with uow:
        review = await uow.review.select_by_id(Review, review_id)
        if review:
            return review.to_dict()
        return None


async def get_reviews_by_ids(
    uow: UnitOfWork,
    ride_id: int = None,
    user_id: int = None,
    driver_id: int = None,
):
    async with uow:
        if ride_id:
            reviews = await uow.review.find_by_ride_id(ride_id)
        elif user_id:
            reviews = await uow.review.find_by_user_id(user_id)
        elif driver_id:
            reviews = await uow.review.find_by_driver_id(driver_id)
        else:
            reviews = []
        return [review.to_dict() for review in reviews]


async def search_reviews_by_comment(comment: str) -> List[dict]:
    cursor = db["review"].find({"$text": {"$search": comment}})
    reviews = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        reviews.append(document)
    return reviews
