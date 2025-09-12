from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.dwallet_handlers import (
    CreateDWallet,
    UpdateDWallet,
    DeleteDWallet,
    ChangeBalanceDWallet,
    handle_add_balance_to_dwallet,
    handle_deduct_balance_from_dwallet,
    handle_create_dwallet,
    handle_update_dwallet,
    handle_delete_dwallet,
)
from src.endpoints.views.dwallet_view import get_all_dwallets, get_dwallet_by_id
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import DWalletCreate, DWalletUpdate, ChangeBalanceRequest

router = APIRouter()


@router.post("/dwallets/", status_code=201)
async def create_dwallet(
    dwallet: DWalletCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreateDWallet(**dwallet.dict())
    await handle_create_dwallet(cmd, uow)
    return {"message": "DWallet created successfully"}


@router.put("/dwallets/{dwallet_id}", status_code=200)
async def update_dwallet(
    dwallet_id: int, dwallet: DWalletUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateDWallet(id=dwallet_id, **dwallet.dict())
    await handle_update_dwallet(cmd, uow)
    return {"message": "DWallet updated successfully"}

@router.put("/dwallets/{dwallet_id}/add-balance", status_code=200)
async def add_balance_to_dwallet(
    dwallet_id: int, 
    request: ChangeBalanceRequest, 
    uow: UnitOfWork = Depends(get_uow)
):
    cmd = ChangeBalanceDWallet(id=dwallet_id, amount=request.amount)
    await handle_add_balance_to_dwallet(cmd, uow)
    return {"message": "Balance added successfully"}

@router.put("/dwallets/{dwallet_id}/deduct-balance", status_code=200)
async def deduct_balance_from_dwallet(
    dwallet_id: int, 
    request: ChangeBalanceRequest, 
    uow: UnitOfWork = Depends(get_uow)
):
    cmd = ChangeBalanceDWallet(id=dwallet_id, amount=request.amount)
    await handle_deduct_balance_from_dwallet(cmd, uow)
    return {"message": "Balance deducted successfully"}


@router.delete("/dwallets/{dwallet_id}", status_code=200)
async def delete_dwallet(dwallet_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteDWallet(id=dwallet_id)
    await handle_delete_dwallet(cmd, uow)
    return {"message": "DWallet deleted successfully"}


@router.get("/dwallets/", status_code=200)
async def list_dwallets(uow: UnitOfWork = Depends(get_uow)):
    dwallets = await get_all_dwallets(uow)
    return dwallets


@router.get("/dwallets/{dwallet_id}", status_code=200)
async def get_dwallet(dwallet_id: int, uow: UnitOfWork = Depends(get_uow)):
    dwallet = await get_dwallet_by_id(dwallet_id, uow)
    if not dwallet:
        raise HTTPException(status_code=404, detail="DWallet not found")
    return dwallet
