from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.user_discounts import UserDiscount
from sqlalchemy import text


class UserDiscountSqlalchemyRepository(AbstractSqlalchemyRepository):
    async def select_by_user_id(self, user_id: int) -> list[UserDiscount]:
        table = UserDiscount.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE user_id = :user_id")
        result = await self._session.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        return [UserDiscount.factory(**r._mapping) for r in rows]
