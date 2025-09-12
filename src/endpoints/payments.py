from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.command_handlers.payments_handlers import (
    CreatePayment,
    UpdatePayment,
    DeletePayment,
    handle_create_payment,
    handle_update_payment,
    handle_delete_payment,
)
from src.endpoints.views.payments_view import get_all_payments, get_payment_by_id
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import PaymentCreate, PaymentUpdate

router = APIRouter()


@router.post("/payments/", status_code=201)
async def create_payment(
    payment: PaymentCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreatePayment(**payment.dict())
    await handle_create_payment(cmd, uow)
    return {"message": "Payment created successfully"}


@router.put("/payments/{payment_id}", status_code=200)
async def update_payment(
    payment_id: int, payment: PaymentUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdatePayment(id=payment_id, **payment.dict())
    await handle_update_payment(cmd, uow)
    return {"message": "Payment updated successfully"}


@router.delete("/payments/{payment_id}", status_code=200)
async def delete_payment(payment_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeletePayment(id=payment_id)
    await handle_delete_payment(cmd, uow)
    return {"message": "Payment deleted successfully"}


@router.get("/payments/", status_code=200)
async def list_payments(uow: UnitOfWork = Depends(get_uow)):
    payments = await get_all_payments(uow)
    return payments


@router.get("/payments/{payment_id}", status_code=200)
async def get_payment(payment_id: int, uow: UnitOfWork = Depends(get_uow)):
    payment = await get_payment_by_id(payment_id, uow)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
