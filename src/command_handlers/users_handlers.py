from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.users import User
from fastapi import HTTPException


@dataclass
class CreateUser:
    phone: str
    first_name: str
    last_name: str


@dataclass
class UpdateUser:
    id: int
    phone: str
    first_name: str
    last_name: str


@dataclass
class DeleteUser:
    id: int


async def handle_create_user(command: CreateUser, uow: UnitOfWork):
    async with uow:
        user = User(
            phone=command.phone,
            first_name=command.first_name,
            last_name=command.last_name,
        )
        await uow.user.insert(user)


async def handle_update_user(command: UpdateUser, uow: UnitOfWork):
    async with uow:
        user = await uow.user.select_by_id(User, command.id)
        if not user:
            raise HTTPException(404,'there is not any user with given id')
        user.update(
            phone=command.phone,
            first_name=command.first_name,
            last_name=command.last_name,
        )
        await uow.user.update(user)


async def handle_delete_user(command: DeleteUser, uow: UnitOfWork):
    async with uow:
        user = await uow.user.select_by_id(User, command.id)
        if not user:
            raise HTTPException(404,'there is not any user with given id')
        await uow.user.delete(user)
