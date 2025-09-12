from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.rides import Ride
from sqlalchemy import text


class RideSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_user_id(self, user_id: int) -> list[Ride]:
        table = Ride.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE user_id = :user_id")
        result = await self._session.execute(query, {"user_id": user_id})
        rows = result.fetchall()  
        return [Ride.factory(**r._mapping) for r in rows]

    async def find_by_driver_id(self, driver_id: int) -> list[Ride]:
        table = Ride.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE driver_id = :driver_id")
        result = await self._session.execute(query, {"driver_id": driver_id})
        rows = result.fetchall()
        return [Ride.factory(**r._mapping) for r in rows]

    async def find_by_canceller_id(self, canceller_id: int) -> list[Ride]:
        table = Ride.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE canceller_id = :canceller_id")
        result = await self._session.execute(query, {"canceller_id": canceller_id})
        rows = result.fetchall()
        return [Ride.factory(**r._mapping) for r in rows]

    async def find_by_driver_and_user(self, driver_id: int, user_id: int) -> list[Ride]:
        table = Ride.entity_type().value
        query = text(f"""
            SELECT * FROM {table} 
            WHERE driver_id = :driver_id AND user_id = :user_id
        """)
        result = await self._session.execute(query, {"driver_id": driver_id, "user_id": user_id})
        rows = result.fetchall()
        return [Ride.factory(**r._mapping) for r in rows]

