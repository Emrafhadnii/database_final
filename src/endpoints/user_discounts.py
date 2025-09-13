from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.user_discounts_handlers import (
    CreateUserDiscount,
    UpdateUserDiscount,
    DeleteUserDiscount,
    handle_create_user_discount,
    handle_update_user_discount,
    handle_delete_user_discount,
)
from src.endpoints.views.user_discounts_view import (
    get_all_user_discounts,
    get_user_discount_by_id,
    get_user_discounts_by_user_id,
)
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import UserDiscountCreate, UserDiscountUpdate

router = APIRouter()


@router.post("/user_discounts/", status_code=201)
async def create_user_discount(
    user_discount: UserDiscountCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreateUserDiscount(**user_discount.dict())
    await handle_create_user_discount(cmd, uow)
    return {"message": "User discount created successfully"}


@router.put("/user_discounts/{user_discount_id}", status_code=200)
async def update_user_discount(
    user_discount_id: int,
    user_discount: UserDiscountUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    cmd = UpdateUserDiscount(id=user_discount_id, **user_discount.dict())
    await handle_update_user_discount(cmd, uow)
    return {"message": "User discount updated successfully"}


@router.delete("/user_discounts/{user_discount_id}", status_code=200)
async def delete_user_discount(
    user_discount_id: int, uow: UnitOfWork = Depends(get_uow)
):
    cmd = DeleteUserDiscount(id=user_discount_id)
    await handle_delete_user_discount(cmd, uow)
    return {"message": "User discount deleted successfully"}


@router.get("/user_discounts/", status_code=200)
async def list_user_discounts(uow: UnitOfWork = Depends(get_uow)):
    user_discounts = await get_all_user_discounts(uow)
    return user_discounts


@router.get("/user_discounts/{user_discount_id}", status_code=200)
async def get_user_discount(
    user_discount_id: int, uow: UnitOfWork = Depends(get_uow)
):
    user_discount = await get_user_discount_by_id(user_discount_id, uow)
    if not user_discount:
        raise HTTPException(status_code=404, detail="User discount not found")
    return user_discount


@router.get("/user_discounts/user/{user_id}", status_code=200)
async def get_user_discounts_by_user(
    user_id: int, uow: UnitOfWork = Depends(get_uow)
):
    user_discounts = await get_user_discounts_by_user_id(user_id, uow)
    return user_discounts
