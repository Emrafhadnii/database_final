from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.discounts import Discount
from sqlalchemy import text
from datetime import datetime, UTC, timedelta


class DiscountSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def expiring_within_one_day(self) -> list[Discount]:
        table = Discount.entity_type().value
        query = text(f"""
            SELECT * FROM {table}
            WHERE expire_time > :now
            AND expire_time <= :next_day
        """)
        now = datetime.now(UTC)
        next_day = now + timedelta(days=1)
        result = await self._session.execute(query, {"now": now, "next_day": next_day})
        rows = result.fetchall()  
        return [Discount.factory(**r._mapping) for r in rows]

    async def expired(self) -> list[Discount]:
        table = Discount.entity_type().value
        query = text(f"""
            SELECT * FROM {table}
            WHERE expire_time <= :now
        """)
        now = datetime.now(UTC)
        result = await self._session.execute(query, {"now": now})
        rows = result.fetchall()
        return [Discount.factory(**r._mapping) for r in rows]

    async def by_ride_type(self, ride_type: str) -> list[Discount]:
        table = Discount.entity_type().value
        query = text(f"""
            SELECT * FROM {table}
            WHERE ride_type = :ride_type
        """)
        result = await self._session.execute(query, {"ride_type": ride_type})
        rows = result.fetchall()
        return [Discount.factory(**r._mapping) for r in rows]

