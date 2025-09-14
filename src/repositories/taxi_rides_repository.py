from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.taxi_rides import TaxiRide
from sqlalchemy import text


class TaxiRideSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_ride_id(self, ride_id: int) -> TaxiRide | None:
        table = TaxiRide.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ride_id = :ride_id")
        result = await self._session.execute(query, {"ride_id": ride_id})
        row = result.fetchone()
        if not row:
            return None
        return TaxiRide.factory(**row._mapping)
