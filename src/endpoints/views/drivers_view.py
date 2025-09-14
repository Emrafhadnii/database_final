from src.service_layer.unit_of_work import UnitOfWork
from src.models.drivers import Driver
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_drivers(uow: UnitOfWork):
    async with uow:
        drivers = await uow.driver.select_all(Driver)
        return [driver.to_dict() for driver in drivers]


async def get_driver_by_id(driver_id: int, uow: UnitOfWork):
    key = f"{Driver.entity_type()}:{driver_id}"
    cached_driver = await redis_dependency.get(key)
    if cached_driver:
        return json.loads(cached_driver)

    async with uow:
        driver = await uow.driver.select_by_id(Driver, driver_id)
        if driver:
            driver_dict = driver.to_dict()
            await redis_dependency.set(key, json.dumps(driver_dict), ex=3600)
            return driver_dict
        raise HTTPException(404, "there is not any driver with given id")


async def get_online_drivers(uow: UnitOfWork):
    async with uow:
        drivers = await uow.driver.select_online_drivers()
        return [driver.to_dict() for driver in drivers]
