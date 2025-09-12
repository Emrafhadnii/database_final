from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.vehicles_handlers import (
    CreateVehicle,
    UpdateVehicle,
    DeleteVehicle,
    handle_create_vehicle,
    handle_update_vehicle,
    handle_delete_vehicle,
)
from src.endpoints.views.vehicles_view import get_all_vehicles, get_vehicle_by_id
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import VehicleCreate, VehicleUpdate

router = APIRouter()


@router.post("/vehicles/", status_code=201)
async def create_vehicle(
    vehicle: VehicleCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreateVehicle(
        owner_id=vehicle.owner_id,
        model=vehicle.model,
        year=vehicle.year,
        license_plate=vehicle.license_plate,
        vehicle_type=vehicle.vehicle_type,
    )
    await handle_create_vehicle(cmd, uow)
    return {"message": "Vehicle created successfully"}


@router.put("/vehicles/{vehicle_id}", status_code=200)
async def update_vehicle(
    vehicle_id: int, vehicle: VehicleUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateVehicle(
        id=vehicle_id,
        owner_id=vehicle.owner_id,
    )
    await handle_update_vehicle(cmd, uow)
    return {"message": "Vehicle updated successfully"}


@router.delete("/vehicles/{vehicle_id}", status_code=200)
async def delete_vehicle(vehicle_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteVehicle(id=vehicle_id)
    await handle_delete_vehicle(cmd, uow)
    return {"message": "Vehicle deleted successfully"}


@router.get("/vehicles/", status_code=200)
async def list_vehicles(uow: UnitOfWork = Depends(get_uow)):
    vehicles = await get_all_vehicles(uow)
    return vehicles


@router.get("/vehicles/{vehicle_id}", status_code=200)
async def get_vehicle(vehicle_id: int, uow: UnitOfWork = Depends(get_uow)):
    vehicle = await get_vehicle_by_id(vehicle_id, uow)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
