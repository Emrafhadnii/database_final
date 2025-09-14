from src.service_layer.unit_of_work import UnitOfWork
from src.models.payments import Payment
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_payments(uow: UnitOfWork):
    async with uow:
        payments = await uow.payment.select_all(Payment)
        return [payment.to_dict() for payment in payments]


async def get_payment_by_id(payment_id: int, uow: UnitOfWork):
    key = f"{Payment.entity_type()}:{payment_id}"
    cached_payment = await redis_dependency.get(key)
    if cached_payment:
        return json.loads(cached_payment)

    async with uow:
        payment = await uow.payment.select_by_id(Payment, payment_id)
        if payment:
            payment_dict = payment.to_dict()
            await redis_dependency.set(key, json.dumps(payment_dict), ex=3600)
            return payment_dict
        raise HTTPException(404, "there is not any payment with given id")
