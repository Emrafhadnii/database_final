from src.service_layer.unit_of_work import UnitOfWork
from src.models.complaints import Complaint
from typing import List
from config.mongo_db import db
from src.endpoints.dependencies.redis_dependency import redis_dependency
from fastapi import HTTPException
import json


async def get_all_complaints(uow: UnitOfWork):
    async with uow:
        complaints = await uow.complaint.select_all(Complaint)
        return [complaint.to_dict() for complaint in complaints]


async def get_complaint_by_id(complaint_id: int, uow: UnitOfWork):
    key = f"{Complaint.entity_type()}:{complaint_id}"
    cached_complaint = await redis_dependency.get(key)
    if cached_complaint:
        return json.loads(cached_complaint)

    async with uow:
        complaint = await uow.complaint.select_by_id(Complaint, complaint_id)
        if complaint:
            complaint_dict = complaint.to_dict()
            await redis_dependency.set(key, json.dumps(complaint_dict), ex=3600)
            return complaint_dict
        raise HTTPException(404, "there is not any complaint with given id")


async def search_complaints_by_reason(reason: str) -> List[dict]:
    cursor = db["complaint"].find({"$text": {"$search": reason}})
    complaints = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        complaints.append(document)
    return complaints
