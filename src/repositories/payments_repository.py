from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.payments import Payment
from sqlalchemy import text


class PaymentSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_ride_id(self, ride_id: int) -> list[Payment]:
        table = Payment.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ride_id = :ride_id")
        result = await self._session.execute(query, {"ride_id": ride_id})
        rows = result.fetchall()  
        return [Payment.factory(**r._mapping) for r in rows]

    async def find_by_user_id(self, user_id: int) -> list[Payment]:
        table = Payment.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE user_id = :user_id")
        result = await self._session.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        return [Payment.factory(**r._mapping) for r in rows]

    async def find_by_user_and_ride(self, user_id: int, ride_id: int) -> list[Payment]:
        table = Payment.entity_type().value
        query = text(f"""
            SELECT * FROM {table} 
            WHERE user_id = :user_id AND ride_id = :ride_id
        """)
        result = await self._session.execute(query, {"user_id": user_id, "ride_id": ride_id})
        rows = result.fetchall()
        return [Payment.factory(**r._mapping) for r in rows]

    async def find_by_transaction_id(self, transaction_id: str) -> Payment | None:
        table = Payment.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE transaction_id = :transaction_id")
        result = await self._session.execute(query, {"transaction_id": transaction_id})
        row = result.fetchone()  
        if not row:
            return None
        return Payment.factory(**row._mapping)

