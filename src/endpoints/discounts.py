from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.discounts_handlers import (
    CreateDiscount,
    UpdateDiscount,
    DeleteDiscount,
    handle_create_discount,
    handle_update_discount,
    handle_delete_discount,
)
from src.endpoints.views.discounts_view import get_all_discounts, get_discount_by_id
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import DiscountCreate, DiscountUpdate

router = APIRouter()


@router.post("/discounts/", status_code=201)
async def create_discount(
    discount: DiscountCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreateDiscount(**discount.dict())
    await handle_create_discount(cmd, uow)
    return {"message": "Discount created successfully"}


@router.put("/discounts/{discount_id}", status_code=200)
async def update_discount(
    discount_id: int, discount: DiscountUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateDiscount(id=discount_id, **discount.dict())
    await handle_update_discount(cmd, uow)
    return {"message": "Discount updated successfully"}


@router.delete("/discounts/{discount_id}", status_code=200)
async def delete_discount(discount_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteDiscount(id=discount_id)
    await handle_delete_discount(cmd, uow)
    return {"message": "Discount deleted successfully"}


@router.get("/discounts/", status_code=200)
async def list_discounts(uow: UnitOfWork = Depends(get_uow)):
    discounts = await get_all_discounts(uow)
    return discounts


@router.get("/discounts/{discount_id}", status_code=200)
async def get_discount(discount_id: int, uow: UnitOfWork = Depends(get_uow)):
    discount = await get_discount_by_id(discount_id, uow)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount
