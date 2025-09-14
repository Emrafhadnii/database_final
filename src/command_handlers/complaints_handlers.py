from dataclasses import dataclass
from src.service_layer.unit_of_work import UnitOfWork
from src.models.complaints import Complaint
from fastapi import HTTPException
from src.endpoints.dependencies.redis_dependency import redis_dependency
import json


@dataclass
class CreateComplaint:
    driver_id: int
    user_id: int
    reasons: str


@dataclass
class UpdateComplaint:
    id: int
    reasons: str


@dataclass
class DeleteComplaint:
    id: int


from src.endpoints.dependencies.bus_dependency import messagebus
from src.events import ComplaintCreated


async def handle_create_complaint(command: CreateComplaint, uow: UnitOfWork):
    async with uow:
        complaint = Complaint(
            driver_id=command.driver_id,
            user_id=command.user_id,
            reasons=command.reasons,
        )
        await uow.complaint.insert(complaint)

        event = ComplaintCreated(
            id=complaint.id,
            user_id=complaint.user_id,
            driver_id=complaint.driver_id,
            reasons=complaint.reasons,
        )

        await messagebus.publish(
            "complaint_created",
            event.dict()
        )


async def handle_update_complaint(command: UpdateComplaint, uow: UnitOfWork):
    async with uow:
        complaint = await uow.complaint.select_by_id(Complaint, command.id)
        if not complaint:
            raise HTTPException(404, "entity not found")
        complaint.update(
            reasons=command.reasons,
        )
        await uow.complaint.update(complaint)
        await redis_dependency.set(f"{Complaint.entity_type()}:{command.id}", json.dumps(complaint.to_dict()), ex=3600)


async def handle_delete_complaint(command: DeleteComplaint, uow: UnitOfWork):
    async with uow:
        complaint = await uow.complaint.select_by_id(Complaint, command.id)
        if not complaint:
            raise HTTPException(404, "entity not found")
        await uow.complaint.delete(complaint)
        await redis_dependency.delete(f"{Complaint.entity_type()}:{command.id}")
