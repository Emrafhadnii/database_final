from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.box_rides import BoxRide
from sqlalchemy import text


class BoxRideSqlalchemyRepository(AbstractSqlalchemyRepository):
    
    async def find_by_ride_id(self, ride_id: int) -> BoxRide | None:
        table = BoxRide.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ride_id = :ride_id")
        result = await self._session.execute(query, {"ride_id": ride_id})
        row = result.fetchone()
        if not row:
            return None
        return BoxRide.factory(**row._mapping)
