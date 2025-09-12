from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.discounts import Discount
from src.models.enums import DiscountType
from datetime import datetime
from fastapi import HTTPException


@dataclass
class CreateDiscount:
    expire_time: datetime
    code: str
    percentage: float | None = None
    amount: int | None = None
    ride_type: DiscountType | None = DiscountType.ALL


@dataclass
class UpdateDiscount:
    id: int
    expire_time: datetime | None = None
    percentage: float | None = None
    amount: int | None = None
    ride_type: DiscountType | None = None


@dataclass
class DeleteDiscount:
    id: int


async def handle_create_discount(command: CreateDiscount, uow: UnitOfWork):
    async with uow:
        discount = Discount(
            expire_time=command.expire_time,
            code=command.code,
            percentage=command.percentage,
            amount=command.amount,
            ride_type=command.ride_type,
        )
        await uow.discount.insert(discount)


async def handle_update_discount(command: UpdateDiscount, uow: UnitOfWork):
    async with uow:
        discount = await uow.discount.select_by_id(Discount, command.id)
        if not discount:
            raise HTTPException(404, "entity not found")
        discount.update(
            expire_time=command.expire_time,
            percentage=command.percentage,
            amount=command.amount,
            ride_type=command.ride_type,
        )
        await uow.discount.update(discount)


async def handle_delete_discount(command: DeleteDiscount, uow: UnitOfWork):
    async with uow:
        discount = await uow.discount.select_by_id(Discount, command.id)
        if not discount:
            raise HTTPException(404, "entity not found")
        await uow.discount.delete(discount)
