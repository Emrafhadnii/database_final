from src.service_layer.unit_of_work import UnitOfWork
from src.models.user_discounts import UserDiscount
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_user_discounts(uow: UnitOfWork):
    async with uow:
        user_discounts = await uow.user_discount.select_all(UserDiscount)
        return [ud.to_dict() for ud in user_discounts]


async def get_user_discount_by_id(user_discount_id: int, uow: UnitOfWork):
    key = f"{UserDiscount.entity_type()}:{user_discount_id}"
    cached_user_discount = await redis_dependency.get(key)
    if cached_user_discount:
        return json.loads(cached_user_discount)

    async with uow:
        user_discount = await uow.user_discount.select_by_id(
            UserDiscount, user_discount_id
        )
        if user_discount:
            user_discount_dict = user_discount.to_dict()
            await redis_dependency.set(key, json.dumps(user_discount_dict), ex=3600)
            return user_discount_dict
        raise HTTPException(404, "there is not any user_discount with given id")


async def get_user_discounts_by_user_id(user_id: int, uow: UnitOfWork):
    async with uow:
        user_discounts = await uow.user_discount.select_by_user_id(user_id)
        return [ud.to_dict() for ud in user_discounts]
