from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.rides import Ride
from src.models.enums import RideType, RideStatus
from datetime import time
from fastapi import HTTPException


@dataclass
class CreateRide:
    user_id: int
    start_address: str
    end_address: str
    ride_type: RideType
    fare: int
    driver_id: int | None = None
    canceller_id: int | None = None
    alternative_end_address: str | None = None
    stop_time: time | None = None


@dataclass
class UpdateRideFare:
    id: int
    fare: int


@dataclass
class UpdateRideEndAddress:
    id: int
    end_address: str


@dataclass
class UpdateRideStartAddress:
    id: int
    start_address: str


@dataclass
class UpdateRideAlternativeEndAddress:
    id: int
    alternative_end_address: str


@dataclass
class UpdateRideStopTime:
    id: int
    stop_time: time


@dataclass
class CancelRide:
    id: int
    canceller_id: int


@dataclass
class AcceptRide:
    id: int
    driver_id: int


@dataclass
class CompleteRide:
    id: int


@dataclass
class StartRide:
    id: int


@dataclass
class UseDiscount:
    id: int
    discount_id: int


@dataclass
class DeleteRide:
    id: int

async def handle_create_ride(command: CreateRide, uow: UnitOfWork):
    async with uow:
        ride = Ride(
            user_id=command.user_id,
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            fare=command.fare,
            driver_id=command.driver_id,
            canceller_id=command.canceller_id,
            alternative_end_address=command.alternative_end_address,
            stop_time=command.stop_time,
        )
        await uow.ride.insert(ride)


async def handle_update_ride_fare(command: UpdateRideFare, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_fare(fare=command.fare)
        await uow.ride.update(ride)


async def handle_update_ride_end_address(
    command: UpdateRideEndAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_end_address(end_address=command.end_address)
        await uow.ride.update(ride)


async def handle_update_ride_start_address(
    command: UpdateRideStartAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_start_address(start_address=command.start_address)
        await uow.ride.update(ride)


async def handle_update_ride_alternative_end_address(
    command: UpdateRideAlternativeEndAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_alternative_end_address(
            alternative_end_address=command.alternative_end_address
        )
        await uow.ride.update(ride)


async def handle_update_ride_stop_time(command: UpdateRideStopTime, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_stop_time(stop_time=command.stop_time)
        await uow.ride.update(ride)


async def handle_cancel_ride(command: CancelRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.cancel_ride(canceller_id=command.canceller_id)
        await uow.ride.update(ride)


async def handle_accept_ride(command: AcceptRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.accept_ride(driver_id=command.driver_id)
        await uow.ride.update(ride)


async def handle_complete_ride(command: CompleteRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.ride_completed()
        await uow.ride.update(ride)


async def handle_start_ride(command: StartRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.start_ride()
        await uow.ride.update(ride)


async def handle_use_discount(command: UseDiscount, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.use_discount(discount_id=command.discount_id)
        await uow.ride.update(ride)


async def handle_delete_ride(command: DeleteRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        await uow.ride.delete(ride)
