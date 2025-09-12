from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.vehicles import Vehicle
from sqlalchemy import text


class VehicleSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_owner_id(self, owner_id: int) -> list[Vehicle]:
        table = Vehicle.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE owner_id = :owner_id")
        result = await self._session.execute(query, {"owner_id": owner_id})
        rows = result.fetchall()  
        return [Vehicle.factory(**r._mapping) for r in rows]

    async def find_by_model(self, model: str) -> list[Vehicle]:
        table = Vehicle.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE model = :model")
        result = await self._session.execute(query, {"model": model})
        rows = result.fetchall()
        return [Vehicle.factory(**r._mapping) for r in rows]

    async def find_by_vehicle_type(self, vehicle_type: str) -> list[Vehicle]:
        table = Vehicle.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE vehicle_type = :vehicle_type")
        result = await self._session.execute(query, {"vehicle_type": vehicle_type})
        rows = result.fetchall()
        return [Vehicle.factory(**r._mapping) for r in rows]

    async def find_by_license_plate(self, license_plate: str) -> Vehicle | None:
        table = Vehicle.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE license_plate = :license_plate")
        result = await self._session.execute(query, {"license_plate": license_plate})
        row = result.fetchone()  
        if not row:
            return None
        return Vehicle.factory(**row._mapping)

