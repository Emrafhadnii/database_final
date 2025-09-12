from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.rides_handlers import (
    CreateRide,
    UpdateRideFare,
    UpdateRideEndAddress,
    UpdateRideStartAddress,
    UpdateRideAlternativeEndAddress,
    UpdateRideStopTime,
    CancelRide,
    AcceptRide,
    CompleteRide,
    DeleteRide,
    handle_create_ride,
    handle_update_ride_fare,
    handle_update_ride_end_address,
    handle_update_ride_start_address,
    handle_update_ride_alternative_end_address,
    handle_update_ride_stop_time,
    handle_cancel_ride,
    handle_accept_ride,
    handle_complete_ride,
    handle_delete_ride,
)
from src.endpoints.views.rides_view import get_all_rides, get_ride_by_id, get_nearby_rides_view
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import RideCreate, RideAccept, RideCancel, RideStatus, RideUpdateAlternativeEndAddress, RideUpdateEndAddress, RideUpdateFare, RideUpdateStartAddress, RideUpdateStopTime

router = APIRouter()


@router.post("/rides/", status_code=201)
async def create_ride(ride: RideCreate, uow: UnitOfWork = Depends(get_uow)):
    cmd = CreateRide(**ride.dict())
    await handle_create_ride(cmd, uow)
    return {"message": "Ride created successfully"}


@router.put("/rides/{ride_id}/fare", status_code=200)
async def update_ride_fare(
    ride_id: int, ride: RideUpdateFare, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateRideFare(id=ride_id, fare=ride.fare)
    await handle_update_ride_fare(cmd, uow)
    return {"message": "Ride fare updated successfully"}


@router.put("/rides/{ride_id}/end-address", status_code=200)
async def update_ride_end_address(
    ride_id: int, ride: RideUpdateEndAddress, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateRideEndAddress(id=ride_id, end_address=ride.end_address)
    await handle_update_ride_end_address(cmd, uow)
    return {"message": "Ride end address updated successfully"}


@router.put("/rides/{ride_id}/start-address", status_code=200)
async def update_ride_start_address(
    ride_id: int, ride: RideUpdateStartAddress, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateRideStartAddress(id=ride_id, start_address=ride.start_address)
    await handle_update_ride_start_address(cmd, uow)
    return {"message": "Ride start address updated successfully"}


@router.put("/rides/{ride_id}/alternative-end-address", status_code=200)
async def update_ride_alternative_end_address(
    ride_id: int,
    ride: RideUpdateAlternativeEndAddress,
    uow: UnitOfWork = Depends(get_uow),
):
    cmd = UpdateRideAlternativeEndAddress(
        id=ride_id, alternative_end_address=ride.alternative_end_address
    )
    await handle_update_ride_alternative_end_address(cmd, uow)
    return {"message": "Ride alternative end address updated successfully"}


@router.put("/rides/{ride_id}/stop-time", status_code=200)
async def update_ride_stop_time(
    ride_id: int, ride: RideUpdateStopTime, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateRideStopTime(id=ride_id, stop_time=ride.stop_time)
    await handle_update_ride_stop_time(cmd, uow)
    return {"message": "Ride stop time updated successfully"}


@router.put("/rides/{ride_id}/cancel", status_code=200)
async def cancel_ride(
    ride_id: int, ride: RideCancel, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CancelRide(id=ride_id, canceller_id=ride.canceller_id)
    await handle_cancel_ride(cmd, uow)
    return {"message": "Ride cancelled successfully"}


@router.put("/rides/{ride_id}/accept", status_code=200)
async def accept_ride(
    ride_id: int, ride: RideAccept, uow: UnitOfWork = Depends(get_uow)
):
    cmd = AcceptRide(id=ride_id, driver_id=ride.driver_id)
    await handle_accept_ride(cmd, uow)
    return {"message": "Ride accepted successfully"}


@router.put("/rides/{ride_id}/complete", status_code=200)
async def complete_ride(ride_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = CompleteRide(id=ride_id)
    await handle_complete_ride(cmd, uow)
    return {"message": "Ride completed successfully"}


@router.delete("/rides/{ride_id}", status_code=200)
async def delete_ride(ride_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteRide(id=ride_id)
    await handle_delete_ride(cmd, uow)
    return {"message": "Ride deleted successfully"}


@router.get("/rides/", status_code=200)
async def list_rides(uow: UnitOfWork = Depends(get_uow)):
    rides = await get_all_rides(uow)
    return rides


@router.get("/rides/{ride_id}", status_code=200)
async def get_ride(ride_id: int, uow: UnitOfWork = Depends(get_uow)):
    ride = await get_ride_by_id(ride_id, uow)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@router.get("rides/")
async def get_nearby_rides(
    lat: float,
    lng: float,
    radius: float,
    uow: UnitOfWork = Depends(get_uow)
):
    nearby_rides = await get_nearby_rides_view(
        lat=lat,
        lng=lng,
        radius=radius,
        uow=uow
    )
    return nearby_rides








