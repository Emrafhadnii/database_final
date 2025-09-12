from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.drivers_handlers import (
    CreateDriver,
    UpdateDriver,
    DeleteDriver,
    handle_create_driver,
    handle_update_driver,
    handle_delete_driver,
)
from src.endpoints.views.drivers_view import get_all_drivers, get_driver_by_id
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import DriverCreate, DriverUpdate

router = APIRouter()


@router.post("/drivers/", status_code=201)
async def create_driver(driver: DriverCreate, uow: UnitOfWork = Depends(get_uow)):
    cmd = CreateDriver(
        na_code=driver.na_code,
        first_name=driver.first_name,
        last_name=driver.last_name,
        ce_code=driver.ce_code,
    )
    await handle_create_driver(cmd, uow)
    return {"message": "Driver created successfully"}


@router.put("/drivers/{driver_id}", status_code=200)
async def update_driver(
    driver_id: int, driver: DriverUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateDriver(
        id=driver_id,
        first_name=driver.first_name,
        last_name=driver.last_name,
    )
    await handle_update_driver(cmd, uow)
    return {"message": "Driver updated successfully"}


@router.delete("/drivers/{driver_id}", status_code=200)
async def delete_driver(driver_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteDriver(id=driver_id)
    await handle_delete_driver(cmd, uow)
    return {"message": "Driver deleted successfully"}


@router.get("/drivers/", status_code=200)
async def list_drivers(uow: UnitOfWork = Depends(get_uow)):
    drivers = await get_all_drivers(uow)
    return drivers


@router.get("/drivers/{driver_id}", status_code=200)
async def get_driver(driver_id: int, uow: UnitOfWork = Depends(get_uow)):
    driver = await get_driver_by_id(driver_id, uow)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
