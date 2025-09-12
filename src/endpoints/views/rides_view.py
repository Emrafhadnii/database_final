from src.service_layer.unit_of_work import UnitOfWork
from src.models.rides import Ride
from sqlalchemy import text


async def get_all_rides(uow: UnitOfWork):
    async with uow:
        rides = await uow.ride.select_all(Ride)
        return [ride.to_dict() for ride in rides]


async def get_ride_by_id(ride_id: int, uow: UnitOfWork):
    async with uow:
        ride = await uow.ride.select_by_id(Ride, ride_id)
        if ride:
            return ride.to_dict()
        return None

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
