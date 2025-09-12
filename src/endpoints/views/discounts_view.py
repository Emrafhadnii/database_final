from src.service_layer.unit_of_work import UnitOfWork
from src.models.discounts import Discount


async def get_all_discounts(uow: UnitOfWork):
    async with uow:
        discounts = await uow.discount.select_all(Discount)
        return [discount.to_dict() for discount in discounts]


async def get_discount_by_id(discount_id: int, uow: UnitOfWork):
    async with uow:
        discount = await uow.discount.select_by_id(Discount, discount_id)
        if discount:
            return discount.to_dict()
        return None
