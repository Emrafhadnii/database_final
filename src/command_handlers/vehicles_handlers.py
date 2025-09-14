from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.vehicles import Vehicle
from src.models.enums import VehicleType
from fastapi import HTTPException
from src.endpoints.dependencies.redis_dependency import redis_dependency
import json


@dataclass
class CreateVehicle:
    owner_id: int
    model: str
    year: int
    license_plate: str
    vehicle_type: VehicleType


@dataclass
class UpdateVehicle:
    id: int
    owner_id: int


@dataclass
class DeleteVehicle:
    id: int


async def handle_create_vehicle(command: CreateVehicle, uow: UnitOfWork):
    async with uow:
        vehicle = Vehicle(
            owner_id=command.owner_id,
            model=command.model,
            year=command.year,
            license_plate=command.license_plate,
            vehicle_type=command.vehicle_type,
        )
        await uow.vehicle.insert(vehicle)


async def handle_update_vehicle(command: UpdateVehicle, uow: UnitOfWork):
    async with uow:
        vehicle = await uow.vehicle.select_by_id(Vehicle, command.id)
        if not vehicle:
            raise HTTPException(404, "entity not found")
        vehicle.update(
            owner_id=command.owner_id,
        )
        await uow.vehicle.update(vehicle)
        await redis_dependency.set(f"{Vehicle.entity_type()}:{command.id}", json.dumps(vehicle.to_dict()), ex=3600)


async def handle_delete_vehicle(command: DeleteVehicle, uow: UnitOfWork):
    async with uow:
        vehicle = await uow.vehicle.select_by_id(Vehicle, command.id)
        if not vehicle:
            raise HTTPException(404, "entity not found")
        await uow.vehicle.delete(vehicle)
        await redis_dependency.delete(f"{Vehicle.entity_type()}:{command.id}")
