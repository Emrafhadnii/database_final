from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.drivers import Driver
from sqlalchemy import text


class DriverSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_na_code(self, na_code: int) -> Driver | None:
        table = Driver.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE na_code = :na_code")
        result = await self._session.execute(query, {"na_code": na_code})
        row = result.fetchone()  
        if not row:
            return None
        return Driver.factory(**row._mapping)

    async def find_by_ce_code(self, ce_code: int) -> Driver | None:
        table = Driver.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE ce_code = :ce_code")
        result = await self._session.execute(query, {"ce_code": ce_code})
        row = result.fetchone()
        if not row:
            return None
        return Driver.factory(**row._mapping)

    async def find_by_full_name(self, name: str) -> list[Driver]:
        table = Driver.entity_type().value
        query = text(f"""
            SELECT * FROM {table}
            WHERE CONCAT(first_name, ' ', last_name) = :full_name
        """)
        result = await self._session.execute(query, {"full_name": name})
        rows = result.fetchall()  
        return [Driver.factory(**r._mapping) for r in rows]

