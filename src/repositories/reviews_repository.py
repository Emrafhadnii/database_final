from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.reviews import Review
from sqlalchemy import text


class ReviewSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_ride_id(self, ride_id: int) -> list[Review]:
        table = Review.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ride_id = :ride_id")
        result = await self._session.execute(query, {"ride_id": ride_id})
        rows = result.fetchall()  
        return [Review.factory(**r._mapping) for r in rows]

    async def find_by_driver_id(self, driver_id: int) -> list[Review]:
        table = Review.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE driver_id = :driver_id")
        result = await self._session.execute(query, {"driver_id": driver_id})
        rows = result.fetchall()
        return [Review.factory(**r._mapping) for r in rows]

    async def find_by_user_id(self, user_id: int) -> list[Review]:
        table = Review.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE user_id = :user_id")
        result = await self._session.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        return [Review.factory(**r._mapping) for r in rows]

