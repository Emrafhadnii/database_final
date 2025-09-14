from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from fastapi import HTTPException
from src.models.rides import Ride
from src.models.discounts import Discount
from src.models.enums import RideType, RideStatus, BoxInsurance, ConsignmentType, TruckInsurance
from src.models.box_rides import BoxRide
from src.models.truck_rides import TruckRide
from src.models.taxi_rides import TaxiRide
from datetime import time
from src.service_layer.fare_calculator import FareCalculator
import json
from src.endpoints.dependencies.redis_dependency import redis_dependency


@dataclass
class CreateTaxiRide:
    user_id: int
    start_address: str
    end_address: str
    ride_type: RideType
    alternative_end_address: str | None = None
    stop_time: time | None = None
    discount_id: int | None = None


@dataclass
class CreateBoxRide:
    user_id: int
    start_address: str
    end_address: str
    ride_type: RideType
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    max_insurance: BoxInsurance
    consignment_type: ConsignmentType
    discount_id: int | None = None


@dataclass
class CreateTruckRide:
    user_id: int
    start_address: str
    end_address: str
    ride_type: RideType
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    max_insurance: TruckInsurance
    has_worker: bool
    discount_id: int | None = None


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


async def handle_create_taxi_ride(command: CreateTaxiRide, uow: UnitOfWork):
    async with uow:
        discount = None
        if command.discount_id:
            discount = await uow.discount.select_by_id(Discount, command.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            alternative_end_address=command.alternative_end_address,
            stop_time=command.stop_time,
            discount=discount,
        )

        ride = Ride(
            user_id=command.user_id,
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            fare=fare,
            discount_id=command.discount_id,
        )
        await uow.ride.insert(ride)

        taxi_ride = TaxiRide(
            ride_id=ride.id,
            alternative_end_address=command.alternative_end_address,
            stop_time=command.stop_time,
        )
        await uow.taxi_ride.insert(taxi_ride)


async def handle_create_box_ride(command: CreateBoxRide, uow: UnitOfWork):
    async with uow:
        discount = None
        if command.discount_id:
            discount = await uow.discount.select_by_id(Discount, command.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            discount=discount,
        )

        ride = Ride(
            user_id=command.user_id,
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            fare=fare,
            discount_id=command.discount_id,
        )
        await uow.ride.insert(ride)

        box_ride = BoxRide(
            ride_id=ride.id,
            sender_name=command.sender_name,
            sender_phone=command.sender_phone,
            recipient_name=command.recipient_name,
            recipient_phone=command.recipient_phone,
            max_insurance=command.max_insurance,
            consignment_type=command.consignment_type,
        )
        await uow.box_ride.insert(box_ride)


async def handle_create_truck_ride(command: CreateTruckRide, uow: UnitOfWork):
    async with uow:
        discount = None
        if command.discount_id:
            discount = await uow.discount.select_by_id(Discount, command.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            discount=discount,
        )

        ride = Ride(
            user_id=command.user_id,
            start_address=command.start_address,
            end_address=command.end_address,
            ride_type=command.ride_type,
            fare=fare,
            discount_id=command.discount_id,
        )
        await uow.ride.insert(ride)

        truck_ride = TruckRide(
            ride_id=ride.id,
            sender_name=command.sender_name,
            sender_phone=command.sender_phone,
            recipient_name=command.recipient_name,
            recipient_phone=command.recipient_phone,
            max_insurance=command.max_insurance,
            has_worker=command.has_worker,
        )
        await uow.truck_ride.insert(truck_ride)


async def handle_update_ride_fare(command: UpdateRideFare, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_fare(fare=command.fare)
        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_update_ride_end_address(
    command: UpdateRideEndAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_end_address(end_address=command.end_address)

        discount = None
        if ride.discount_id:
            discount = await uow.discount.select_by_id(Discount, ride.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=ride.start_address,
            end_address=ride.end_address,
            ride_type=ride.ride_type,
            alternative_end_address=ride.alternative_end_address,
            stop_time=ride.stop_time,
            discount=discount,
        )
        ride.update_fare(fare=fare)

        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_update_ride_start_address(
    command: UpdateRideStartAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.update_start_address(start_address=command.start_address)

        discount = None
        if ride.discount_id:
            discount = await uow.discount.select_by_id(Discount, ride.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=ride.start_address,
            end_address=ride.end_address,
            ride_type=ride.ride_type,
            alternative_end_address=ride.alternative_end_address,
            stop_time=ride.stop_time,
            discount=discount,
        )
        ride.update_fare(fare=fare)

        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_update_ride_alternative_end_address(
    command: UpdateRideAlternativeEndAddress, uow: UnitOfWork
):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        
        taxi_ride = await uow.taxi_ride.find_by_ride_id(ride.id)
        if not taxi_ride:
            raise HTTPException(404, "entity not found")

        taxi_ride.alternative_end_address = command.alternative_end_address
        await uow.taxi_ride.update(taxi_ride)

        discount = None
        if ride.discount_id:
            discount = await uow.discount.select_by_id(Discount, ride.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=ride.start_address,
            end_address=ride.end_address,
            ride_type=ride.ride_type,
            alternative_end_address=taxi_ride.alternative_end_address,
            stop_time=taxi_ride.stop_time,
            discount=discount,
        )
        ride.update_fare(fare=fare)

        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_update_ride_stop_time(command: UpdateRideStopTime, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")

        taxi_ride = await uow.taxi_ride.find_by_ride_id(ride.id)
        if not taxi_ride:
            raise HTTPException(404, "entity not found")

        taxi_ride.stop_time = command.stop_time
        await uow.taxi_ride.update(taxi_ride)

        discount = None
        if ride.discount_id:
            discount = await uow.discount.select_by_id(Discount, ride.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=ride.start_address,
            end_address=ride.end_address,
            ride_type=ride.ride_type,
            alternative_end_address=taxi_ride.alternative_end_address,
            stop_time=taxi_ride.stop_time,
            discount=discount,
        )
        ride.update_fare(fare=fare)

        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_cancel_ride(command: CancelRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.cancel_ride(canceller_id=command.canceller_id)
        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_accept_ride(command: AcceptRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.accept_ride(driver_id=command.driver_id)
        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_complete_ride(command: CompleteRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.ride_completed()
        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_start_ride(command: StartRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.start_ride()
        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_use_discount(command: UseDiscount, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        ride.use_discount(discount_id=command.discount_id)

        discount = None
        if ride.discount_id:
            discount = await uow.discount.select_by_id(Discount, ride.discount_id)

        fare = FareCalculator.calculate_fare(
            start_address=ride.start_address,
            end_address=ride.end_address,
            ride_type=ride.ride_type,
            alternative_end_address=ride.alternative_end_address,
            stop_time=ride.stop_time,
            discount=discount,
        )
        ride.update_fare(fare=fare)

        await uow.ride.update(ride)
        await redis_dependency.set(f"{Ride.entity_type()}:{command.id}", json.dumps(ride.to_dict()), ex=3600)


async def handle_delete_ride(command: DeleteRide, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, command.id)
        if not ride:
            raise HTTPException(404, "entity not found")
        await uow.ride.delete(ride)
        await redis_dependency.delete(f"{Ride.entity_type()}:{command.id}")
