from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.payments import Payment
from src.models.enums import PaymentMethod
from fastapi import HTTPException


@dataclass
class CreatePayment:
    user_id: int
    ride_id: int
    amount: int
    payment_method: PaymentMethod = PaymentMethod.CASH
    transaction_id: str | None = None


@dataclass
class UpdatePayment:
    id: int
    amount: int | None = None
    payment_method: PaymentMethod | None = None


@dataclass
class DeletePayment:
    id: int


async def handle_create_payment(command: CreatePayment, uow: UnitOfWork):
    async with uow:
        payment = Payment(
            user_id=command.user_id,
            ride_id=command.ride_id,
            amount=command.amount,
            payment_method=command.payment_method,
            transaction_id=command.transaction_id,
        )
        await uow.payment.insert(payment)


async def handle_update_payment(command: UpdatePayment, uow: UnitOfWork):
    async with uow:
        payment = await uow.payment.select_by_id(Payment, command.id)
        if not payment:
            raise HTTPException(404, "entity not found")
        payment.update(
            amount=command.amount,
            payment_method=command.payment_method,
        )
        await uow.payment.update(payment)


async def handle_delete_payment(command: DeletePayment, uow: UnitOfWork):
    async with uow:
        payment = await uow.payment.select_by_id(Payment, command.id)
        if not payment:
            raise HTTPException(404, "entity not found")
        await uow.payment.delete(payment)
