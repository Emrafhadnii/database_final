from src.service_layer.unit_of_work import UnitOfWork
from src.models.vehicles import Vehicle
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_vehicles(uow: UnitOfWork):
    async with uow:
        vehicles = await uow.vehicle.select_all(Vehicle)
        return [vehicle.to_dict() for vehicle in vehicles]


async def get_vehicle_by_id(vehicle_id: int, uow: UnitOfWork):
    key = f"{Vehicle.entity_type()}:{vehicle_id}"
    cached_vehicle = await redis_dependency.get(key)
    if cached_vehicle:
        return json.loads(cached_vehicle)

    async with uow:
        vehicle = await uow.vehicle.select_by_id(Vehicle, vehicle_id)
        if vehicle:
            vehicle_dict = vehicle.to_dict()
            await redis_dependency.set(key, json.dumps(vehicle_dict), ex=3600)
            return vehicle_dict
        raise HTTPException(404, "there is not any vehicle with given id")
