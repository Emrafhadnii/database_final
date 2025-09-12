from src.service_layer.unit_of_work import UnitOfWork
from src.models.dwallet import DWallet


async def get_all_dwallets(uow: UnitOfWork):
    async with uow:
        dwallets = await uow.dwallet.select_all(DWallet)
        return [dwallet.to_dict() for dwallet in dwallets]


async def get_dwallet_by_id(dwallet_id: int, uow: UnitOfWork):
    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, dwallet_id)
        if dwallet:
            return dwallet.to_dict()
        return None
