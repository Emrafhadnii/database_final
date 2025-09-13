from pydantic import BaseModel

class ComplaintCreated(BaseModel):
    id: int
    user_id: int
    driver_id: int
    reasons: str

class ReviewCreated(BaseModel):
    id: int
    ride_id: int
    user_id: int
    driver_id: int
    rating: int
    comment: str
