from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.truck_rides import TruckRide
from sqlalchemy import text


class TruckRideSqlalchemyRepository(AbstractSqlalchemyRepository):
    
    async def find_by_ride_id(self, ride_id: int) -> TruckRide | None:
        table = TruckRide.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ride_id = :ride_id")
        result = await self._session.execute(query, {"ride_id": ride_id})
        row = result.fetchone()
        if not row:
            return None
        return TruckRide.factory(**row._mapping)
