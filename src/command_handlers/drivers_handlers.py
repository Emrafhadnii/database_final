from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.drivers import Driver
from fastapi import HTTPException
from src.endpoints.dependencies.redis_dependency import redis_dependency
import json


@dataclass
class CreateDriver:
    na_code: int
    first_name: str
    last_name: str
    ce_code: int


@dataclass
class UpdateDriver:
    id: int
    first_name: str
    last_name: str


@dataclass
class DeleteDriver:
    id: int


@dataclass
class ToggleDriverStatus:
    id: int


async def handle_create_driver(command: CreateDriver, uow: UnitOfWork):
    async with uow:
        driver = Driver(
            na_code=command.na_code,
            first_name=command.first_name,
            last_name=command.last_name,
            ce_code=command.ce_code,
        )
        await uow.driver.insert(driver)


async def handle_update_driver(command: UpdateDriver, uow: UnitOfWork):
    async with uow:
        driver = await uow.driver.select_by_id(Driver, command.id)
        if not driver:
            raise HTTPException(404, "entity not found")
        driver.update(
            first_name=command.first_name,
            last_name=command.last_name,
        )
        await uow.driver.update(driver)
        await redis_dependency.set(f"{Driver.entity_type()}:{command.id}", json.dumps(driver.to_dict()), ex=3600)


async def handle_delete_driver(command: DeleteDriver, uow: UnitOfWork):
    async with uow:
        driver = await uow.driver.select_by_id(Driver, command.id)
        if not driver:
            raise HTTPException(404, "entity not found")
        await uow.driver.delete(driver)
        await redis_dependency.delete(f"{Driver.entity_type()}:{command.id}")


async def handle_toggle_driver_status(command: ToggleDriverStatus, uow: UnitOfWork):
    async with uow:
        driver = await uow.driver.select_by_id(Driver, command.id)
        if not driver:
            raise HTTPException(404, "entity not found")
        driver.toggle_on()
        await uow.driver.update(driver)
        await redis_dependency.delete(f"{Driver.entity_type()}:{command.id}")
