from src.service_layer.unit_of_work import UnitOfWork
from src.models.users import User


async def get_all_users(uow: UnitOfWork):
    async with uow:
        users = await uow.user.select_all(User)
        return [user.to_dict() for user in users]


async def get_user_by_id(user_id: int, uow: UnitOfWork):
    async with uow:
        user = await uow.user.select_by_id(User, user_id)
        if user:
            return user.to_dict()
        return None
