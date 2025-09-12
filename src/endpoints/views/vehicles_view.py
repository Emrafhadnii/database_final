from src.service_layer.unit_of_work import UnitOfWork
from src.models.vehicles import Vehicle


async def get_all_vehicles(uow: UnitOfWork):
    async with uow:
        vehicles = await uow.vehicle.select_all(Vehicle)
        return [vehicle.to_dict() for vehicle in vehicles]


async def get_vehicle_by_id(vehicle_id: int, uow: UnitOfWork):
    async with uow:
        vehicle = await uow.vehicle.select_by_id(Vehicle, vehicle_id)
        if vehicle:
            return vehicle.to_dict()
        return None
