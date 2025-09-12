from abc import ABC, abstractmethod
from .abstract_entity import AbstractEntity

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy import text


class AbstractSqlalchemyRepository(ABC):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def refresh(self, entity) -> None:
        await self._session.refresh(entity)

    async def insert(self, entity: AbstractEntity):
        table = entity.entity_type().value
        data = entity.to_dict()

        exclude = {"id", "created_at", "updated_at"}
        cols = [c for c in data.keys() if c not in exclude]
        vals = [data[c] for c in cols]

        columns = ", ".join(cols)
        placeholders = ", ".join([f":{c}" for c in cols])

        query = text(f"""
            INSERT INTO {table} ({columns}, created_at, updated_at)
            VALUES ({placeholders}, NOW(), NOW())
            RETURNING id
        """)
        result = await self._session.execute(query, dict(zip(cols, vals)))
        entity.id = result.scalar()
        await self._session.flush()


    async def update(self, entity: AbstractEntity):
        table = entity.entity_type().value
        data = entity.to_dict()

        exclude = {"id", "created_at"}
        cols = [c for c in data.keys() if c not in exclude]

        set_clause = ", ".join([f"{c} = :{c}" for c in cols])

        query = text(f"""
            UPDATE {table}
            SET {set_clause}
            WHERE id = :id
        """)
        await self._session.execute(query, data)
        await self._session.flush()
        


    async def select_by_id(self, entity: type[AbstractEntity], entity_id: int):
        table = entity.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE id = :id")
        result = await self._session.execute(query, {"id": entity_id})
        row = result.fetchone()
        if not row:
            return None
        return entity.factory(**row._mapping)

    
    async def select_all(self, entity: type[AbstractEntity]):
        table = entity.entity_type().value
        query = text(f"SELECT * FROM {table}")
        result = await self._session.execute(query)
        rows = result.fetchall()
        return [entity.factory(**row._mapping) for row in rows]

    
    async def delete(self, entity: AbstractEntity):
        table = entity.entity_type().value
        query = text(f"DELETE FROM {table} WHERE id = :id")
        await self._session.execute(query, {"id": entity.id})
        await self._session.flush()

