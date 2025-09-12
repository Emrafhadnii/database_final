from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.command_handlers.users_handlers import (
    CreateUser,
    UpdateUser,
    DeleteUser,
    handle_create_user,
    handle_update_user,
    handle_delete_user,
)
from src.endpoints.views.users_view import get_all_users, get_user_by_id
from src.endpoints.dependencies.uow_dependency import get_uow
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.request_models import UserCreate, UserUpdate

router = APIRouter()

@router.post("/users/", status_code=201)
async def create_user(user: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    cmd = CreateUser(
        phone=user.phone, first_name=user.first_name, last_name=user.last_name
    )
    await handle_create_user(cmd, uow)
    return {"message": "User created successfully"}


@router.put("/users/{user_id}", status_code=200)
async def update_user(
    user_id: int, user: UserUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateUser(
        id=user_id,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    await handle_update_user(cmd, uow)
    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}", status_code=200)
async def delete_user(user_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteUser(id=user_id)
    await handle_delete_user(cmd, uow)
    return {"message": "User deleted successfully"}


@router.get("/users/", status_code=200)
async def list_users(uow: UnitOfWork = Depends(get_uow)):
    users = await get_all_users(uow)
    return users


@router.get("/users/{user_id}", status_code=200)
async def get_user(user_id: int, uow: UnitOfWork = Depends(get_uow)):
    user = await get_user_by_id(user_id, uow)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
