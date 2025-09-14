from src.service_layer.unit_of_work import UnitOfWork
from src.models.rides import Ride
from sqlalchemy import text
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json
from src.models.enums import RideType


async def get_all_rides(uow: UnitOfWork):
    async with uow:
        rides = await uow.ride.select_all(Ride)
        rides_data = []
        for ride in rides:
            ride_dict = ride.to_dict()
            if ride.ride_type == RideType.TAXI:
                taxi_ride = await uow.taxi_ride.find_by_ride_id(ride.id)
                if taxi_ride:
                    ride_dict.update(taxi_ride.to_dict())
            elif ride.ride_type == RideType.BOX:
                box_ride = await uow.box_ride.find_by_ride_id(ride.id)
                if box_ride:
                    ride_dict.update(box_ride.to_dict())
            elif ride.ride_type == RideType.TRUCK:
                truck_ride = await uow.truck_ride.find_by_ride_id(ride.id)
                if truck_ride:
                    ride_dict.update(truck_ride.to_dict())
            rides_data.append(ride_dict)
        return rides_data


async def get_ride_by_id(ride_id: int, uow: UnitOfWork):
    key = f"{Ride.entity_type()}:{ride_id}"
    cached_ride = await redis_dependency.get(key)
    if cached_ride:
        return json.loads(cached_ride)

    async with uow:
        ride = await uow.ride.select_by_id(Ride, ride_id)
        if ride:
            ride_dict = ride.to_dict()
            if ride.ride_type == RideType.TAXI:
                taxi_ride = await uow.taxi_ride.find_by_ride_id(ride.id)
                if taxi_ride:
                    ride_dict.update(taxi_ride.to_dict())
            elif ride.ride_type == RideType.BOX:
                box_ride = await uow.box_ride.find_by_ride_id(ride.id)
                if box_ride:
                    ride_dict.update(box_ride.to_dict())
            elif ride.ride_type == RideType.TRUCK:
                truck_ride = await uow.truck_ride.find_by_ride_id(ride.id)
                if truck_ride:
                    ride_dict.update(truck_ride.to_dict())

            await redis_dependency.set(key, json.dumps(ride_dict), ex=3600)
            return ride_dict
        raise HTTPException(404, "there is not any ride with given id")


async def get_nearby_rides_view(uow: UnitOfWork, lat: float, lng: float, radius: float = 5000):
    async with uow:
        query = text("""
            SELECT r.*
            FROM rides r
            WHERE r.status = 'REQUESTED'
              AND ST_DWithin(
                    r.start_address::geography,
                    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
                    :radius
                  )
        """)

        result = await uow.session.execute(query, {
            "lat": lat,
            "lng": lng,
            "radius": radius
        })
        rows = result.fetchall()

        return [Ride.factory(**row._mapping) for row in rows]
