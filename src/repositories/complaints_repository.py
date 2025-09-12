from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.complaints import Complaint
from sqlalchemy import text


class ComplaintSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_user_id(self, user_id: int) -> list[Complaint]:
        table = Complaint.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE user_id = :user_id")
        result = await self._session.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        return [Complaint.factory(**r._mapping) for r in rows]

    async def find_by_driver_id(self, driver_id: int) -> list[Complaint]:
        table = Complaint.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE driver_id = :driver_id")
        result = await self._session.execute(query, {"driver_id": driver_id})
        rows = result.fetchall()
        return [Complaint.factory(**r._mapping) for r in rows]

    async def find_by_user_and_driver(self, user_id: int, driver_id: int) -> list[Complaint]:
        table = Complaint.entity_type().value
        query = text(f"""
            SELECT * FROM {table} 
            WHERE user_id = :user_id AND driver_id = :driver_id
        """)
        result = await self._session.execute(query, {"user_id": user_id, "driver_id": driver_id})
        rows = result.fetchall()
        return [Complaint.factory(**r._mapping) for r in rows]

