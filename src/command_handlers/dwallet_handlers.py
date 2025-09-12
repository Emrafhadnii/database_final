from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.dwallet import DWallet
from fastapi import HTTPException


@dataclass
class CreateDWallet:
    driver_id: int
    bank_account: str
    balance: int | None = 0


@dataclass
class UpdateDWallet:
    id: int
    bank_account: str


@dataclass
class DeleteDWallet:
    id: int

@dataclass
class ChangeBalanceDWallet:
    id: int
    amount: int


async def handle_create_dwallet(command: CreateDWallet, uow: UnitOfWork):
    async with uow:
        dwallet = DWallet(
            driver_id=command.driver_id,
            bank_account=command.bank_account,
            balance=command.balance,
        )
        await uow.dwallet.insert(dwallet)


async def handle_update_dwallet(command: UpdateDWallet, uow: UnitOfWork):
    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, command.id)
        if not dwallet:
            raise HTTPException(404, "entity not found")
        dwallet.update(
            bank_account=command.bank_account,
        )
        await uow.dwallet.update(dwallet)


async def handle_delete_dwallet(command: DeleteDWallet, uow: UnitOfWork):
    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, command.id)
        if not dwallet:
            raise HTTPException(404, "entity not found")
        await uow.dwallet.delete(dwallet)


async def handle_add_balance_to_dwallet(command: ChangeBalanceDWallet, uow: UnitOfWork):
    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, command.id)
        if not dwallet:
            raise HTTPException(404, "DWallet not found")
        dwallet.add_balance(command.amount)
        await uow.dwallet.update(dwallet)


async def handle_deduct_balance_from_dwallet(command: ChangeBalanceDWallet, uow: UnitOfWork):
    async with uow:
        dwallet = await uow.dwallet.select_by_id(DWallet, command.id)
        if not dwallet:
            raise HTTPException(404, "DWallet not found")
        dwallet.deduct_balance(command.amount)
        await uow.dwallet.update(dwallet)
