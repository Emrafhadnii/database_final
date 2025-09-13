from config.mongo_db import db

async def handle_complaint_created(message: dict):
    document = {
        "id": message["id"],
        "user_id": message["user_id"],
        "driver_id": message["driver_id"],
        "reasons": message["reasons"],
    }
    await db["complaint"].insert_one(document)

async def handle_review_created(message: dict):
    document = {
        "id": message["id"],
        "ride_id": message["ride_id"],
        "user_id": message["user_id"],
        "driver_id": message["driver_id"],
        "rating": message["rating"],
        "comment": message["comment"],
    }
    await db["review"].insert_one(document)
