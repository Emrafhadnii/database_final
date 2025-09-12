from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.users import User
from sqlalchemy import text


class UserSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_phone(self, phone: str) -> User | None:
        table = User.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE phone = :phone")
        result = await self._session.execute(query, {"phone": phone})
        row = result.fetchone()  
        if not row:
            return None
        return User.factory(**row._mapping)

    async def find_by_full_name(self, full_name: str) -> list[User]:
        table = User.entity_type().value
        query = text(f"""
            SELECT * FROM {table} 
            WHERE CONCAT(first_name, ' ', last_name) = :full_name
        """)
        result = await self._session.execute(query, {"full_name": full_name})
        rows = result.fetchall()  
        return [User.factory(**r._mapping) for r in rows]

