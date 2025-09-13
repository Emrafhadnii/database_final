from src.service_layer.unit_of_work import UnitOfWork
from src.models.user_discounts import UserDiscount


async def get_all_user_discounts(uow: UnitOfWork):
    async with uow:
        user_discounts = await uow.user_discount.select_all(UserDiscount)
        return [ud.to_dict() for ud in user_discounts]


async def get_user_discount_by_id(user_discount_id: int, uow: UnitOfWork):
    async with uow:
        user_discount = await uow.user_discount.select_by_id(UserDiscount, user_discount_id)
        if user_discount:
            return user_discount.to_dict()
        return None


async def get_user_discounts_by_user_id(user_id: int, uow: UnitOfWork):
    async with uow:
        user_discounts = await uow.user_discount.select_by_user_id(user_id)
        return [ud.to_dict() for ud in user_discounts]
