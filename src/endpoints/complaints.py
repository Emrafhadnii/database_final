from fastapi import APIRouter, Depends, HTTPException
from src.command_handlers.complaints_handlers import (
    CreateComplaint,
    UpdateComplaint,
    DeleteComplaint,
    handle_create_complaint,
    handle_update_complaint,
    handle_delete_complaint,
)
from src.endpoints.views.complaints_view import (
    get_all_complaints,
    get_complaint_by_id,
)
from src.service_layer.unit_of_work import UnitOfWork
from src.endpoints.dependencies.uow_dependency import get_uow
from src.endpoints.request_models import ComplaintCreate, ComplaintUpdate

router = APIRouter()


@router.post("/complaints/", status_code=201)
async def create_complaint(
    complaint: ComplaintCreate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = CreateComplaint(**complaint.dict())
    await handle_create_complaint(cmd, uow)
    return {"message": "Complaint created successfully"}


@router.put("/complaints/{complaint_id}", status_code=200)
async def update_complaint(
    complaint_id: int, complaint: ComplaintUpdate, uow: UnitOfWork = Depends(get_uow)
):
    cmd = UpdateComplaint(id=complaint_id, **complaint.dict())
    await handle_update_complaint(cmd, uow)
    return {"message": "Complaint updated successfully"}


@router.delete("/complaints/{complaint_id}", status_code=200)
async def delete_complaint(complaint_id: int, uow: UnitOfWork = Depends(get_uow)):
    cmd = DeleteComplaint(id=complaint_id)
    await handle_delete_complaint(cmd, uow)
    return {"message": "Complaint deleted successfully"}


@router.get("/complaints/", status_code=200)
async def list_complaints(uow: UnitOfWork = Depends(get_uow)):
    complaints = await get_all_complaints(uow)
    return complaints


@router.get("/complaints/{complaint_id}", status_code=200)
async def get_complaint(complaint_id: int, uow: UnitOfWork = Depends(get_uow)):
    complaint = await get_complaint_by_id(complaint_id, uow)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint
