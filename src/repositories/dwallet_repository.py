from ..shared.abstract_repository import AbstractSqlalchemyRepository
from ..models.dwallet import DWallet
from sqlalchemy import text


class DWalletSqlalchemyRepository(AbstractSqlalchemyRepository):

    async def find_by_driver_id(self, driver_id: int) -> list[DWallet]:
        table = DWallet.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE driver_id = :driver_id")
        result = await self._session.execute(query, {"driver_id": driver_id})
        rows = result.fetchall()  
        return [DWallet.factory(**r._mapping) for r in rows]

    async def find_by_bank_account(self, bank_account: str) -> DWallet | None:
        table = DWallet.entity_type().value
        query = text(f"SELECT * FROM {table} WHERE bank_account = :bank_account")
        result = await self._session.execute(query, {"bank_account": bank_account})
        row = result.fetchone()  
        if not row:
            return None
        return DWallet.factory(**row._mapping)

