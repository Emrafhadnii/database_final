from src.service_layer.unit_of_work import UnitOfWork
from src.models.complaints import Complaint


async def get_all_complaints(uow: UnitOfWork):
    async with uow:
        complaints = await uow.complaint.select_all(Complaint)
        return [complaint.to_dict() for complaint in complaints]


async def get_complaint_by_id(complaint__id: int, uow: UnitOfWork):
    async with uow:
        complaint = await uow.complaint.select_by_id(Complaint, complaint_id)
        if complaint:
            return complaint.to_dict()
        return None
