from src.service_layer.unit_of_work import UnitOfWork
from src.models.discounts import Discount
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_discounts(uow: UnitOfWork):
    async with uow:
        discounts = await uow.discount.select_all(Discount)
        return [discount.to_dict() for discount in discounts]


async def get_discount_by_id(discount_id: int, uow: UnitOfWork):
    key = f"{Discount.entity_type()}:{discount_id}"
    cached_discount = await redis_dependency.get(key)
    if cached_discount:
        return json.loads(cached_discount)

    async with uow:
        discount = await uow.discount.select_by_id(Discount, discount_id)
        if discount:
            discount_dict = discount.to_dict()
            await redis_dependency.set(key, json.dumps(discount_dict), ex=3600)
            return discount_dict
        raise HTTPException(404, "there is not any discount with given id")
