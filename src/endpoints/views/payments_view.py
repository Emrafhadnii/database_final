from src.service_layer.unit_of_work import UnitOfWork
from src.models.payments import Payment


async def get_all_payments(uow: UnitOfWork):
    async with uow:
        payments = await uow.payment.select_all(Payment)
        return [payment.to_dict() for payment in payments]


async def get_payment_by_id(payment_id: int, uow: UnitOfWork):
    async with uow:
        payment = await uow.payment.select_by_id(Payment, payment_id)
        if payment:
            return payment.to_dict()
        return None
