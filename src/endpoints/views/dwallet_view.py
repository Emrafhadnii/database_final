from src.service_layer.unit_of_work import UnitOfWork
from src.models.dwallet import DWallet
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_dwallets(uow: UnitOfWork):
    async with uow:
        dwallets = await uow.dwallet.select_all(DWallet)
        return [dwallet.to_dict() for dwallet in dwallets]


async def get_dwallet_by_id(dwallet_id: int, uow: UnitOfWork):
    key = f"{DWallet.entity_type()}:{dwallet_id}"
    cached_dwallet = await redis_dependency.get(key)
    if cached_dwallet:
        return json.loads(cached_dwallet)

    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, dwallet_id)
        if dwallet:
            dwallet_dict = dwallet.to_dict()
            await redis_dependency.set(key, json.dumps(dwallet_dict), ex=3600)
            return dwallet_dict
        raise HTTPException(404, "there is not any dwallet with given id")
