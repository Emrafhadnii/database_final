from src.service_layer.unit_of_work import UnitOfWork
from src.models.users import User
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_users(uow: UnitOfWork):
    async with uow:
        users = await uow.user.select_all(User)
        return [user.to_dict() for user in users]


async def get_user_by_id(user_id: int, uow: UnitOfWork):
    key = f"{User.entity_type()}:{user_id}"
    cached_user = await redis_dependency.get(key)
    if cached_user:
        return json.loads(cached_user)

    async with uow:
        user = await uow.user.select_by_id(User, user_id)
        if user:
            user_dict = user.to_dict()
            await redis_dependency.set(key, json.dumps(user_dict), ex=3600)
            return user_dict
        raise HTTPException(404, "there is not any user with given id")
