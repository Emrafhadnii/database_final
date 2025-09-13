from fastapi import APIRouter, Depends, HTTPException, Query
from src.command_handlers.reviews_handlers import (
    CreateReview,
    UpdateReview,
    DeleteReview,
    handle_create_review,
    handle_update_review,
    handle_delete_review,
)
from src.endpoints.views.reviews_view import get_all_reviews, get_review_by_id, search_reviews_by_comment, get_reviews_by_ids
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import ReviewCreate, ReviewUpdate
from typing import Optional

router = APIRouter()



@router.post("/reviews/", status_code=201)
async def create_review(review: ReviewCreate, uow: UnitOfWork = Depends(get_uow)):
    cmd = CreateReview(**review.dict())
    await handle_create_review(cmd, uow)
    return {"message": "Review created successfully"}


@router.put("/reviews/{review_id}", status_code=200)
async def update_review(
    review_id: int, review: ReviewUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateReview(id=review_id, **review.dict())
    await handle_update_review(cmd, uow)
    return {"message": "Review updated successfully"}


@router.delete("/reviews/{review_id}", status_code=200)
async def delete_review(review_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteReview(id=review_id)
    await handle_delete_review(cmd, uow)
    return {"message": "Review deleted successfully"}


@router.get("/reviews/", status_code=200)
async def list_reviews(uow: UnitOfWork = Depends(get_uow)):
    reviews = await get_all_reviews(uow)
    return reviews


@router.get("/reviews/filter/", status_code=200)
async def list_reviews_by_ids(
    ride_id: Optional[int] = None,
    user_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    uow: UnitOfWork = Depends(get_uow),
):
    if len([arg for arg in [ride_id, user_id, driver_id] if arg is not None]) > 1:
        raise HTTPException(
            status_code=400, detail="Only one of ride_id, user_id, or driver_id can be provided."
        )
    reviews = await get_reviews_by_ids(uow, ride_id, user_id, driver_id)
    return reviews


@router.get("/reviews/{review_id}", status_code=200)
async def get_review(review_id: int, uow: UnitOfWork = Depends(get_uow)):
    review = await get_review_by_id(review_id, uow)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/reviews/search/", status_code=200)
async def search_reviews(comment: str = Query(..., min_length=3, max_length=50)):
    reviews = await search_reviews_by_comment(comment)
    return reviews
