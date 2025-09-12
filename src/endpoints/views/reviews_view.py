from src.service_layer.unit_of_work import UnitOfWork
from src.models.reviews import Review


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
