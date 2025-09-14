from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.user_discounts import UserDiscount
from fastapi import HTTPException
from src.endpoints.dependencies.redis_dependency import redis_dependency
import json


@dataclass
class CreateUserDiscount:
    user_id: int
    discount_id: int


@dataclass
class UpdateUserDiscount:
    id: int
    used: bool


@dataclass
class DeleteUserDiscount:
    id: int


async def handle_create_user_discount(command: CreateUserDiscount, uow: UnitOfWork):
    async with uow:
        user_discount = UserDiscount(
            user_id=command.user_id,
            discount_id=command.discount_id,
        )
        await uow.user_discount.insert(user_discount)


async def handle_update_user_discount(command: UpdateUserDiscount, uow: UnitOfWork):
    async with uow:
        user_discount = await uow.user_discount.select_by_id(UserDiscount, command.id)
        if not user_discount:
            raise HTTPException(404, "entity not found")
        if command.used:
            user_discount.use()
        await uow.user_discount.update(user_discount)
        await redis_dependency.set(f"{UserDiscount.entity_type()}:{command.id}", json.dumps(user_discount.to_dict()), ex=3600)


async def handle_delete_user_discount(command: DeleteUserDiscount, uow: UnitOfWork):
    async with uow:
        user_discount = await uow.user_discount.select_by_id(UserDiscount, command.id)
        if not user_discount:
            raise HTTPException(404, "entity not found")
        await uow.user_discount.delete(user_discount)
        await redis_dependency.delete(f"{UserDiscount.entity_type()}:{command.id}")
