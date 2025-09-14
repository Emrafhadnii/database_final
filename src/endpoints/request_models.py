from pydantic import BaseModel
from src.models.enums import VehicleType, PaymentMethod, RideType, RideStatus, DiscountType
from datetime import time, datetime

class UserCreate(BaseModel):
    phone: str
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    phone: str
    first_name: str
    last_name: str

class VehicleCreate(BaseModel):
    owner_id: int
    model: str
    year: int
    license_plate: str
    vehicle_type: VehicleType


class VehicleUpdate(BaseModel):
    owner_id: int


class RideCreate(BaseModel):
    user_id: int
    start_address: str
    end_address: str
    discount_id: int | None = None


class TaxiRideCreate(RideCreate):
    ride_type: RideType = RideType.TAXI
    alternative_end_address: str | None = None
    stop_time: time | None = None


class BoxRideCreate(RideCreate):
    ride_type: RideType = RideType.BOX
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    max_insurance: str
    consignment_type: str


class TruckRideCreate(RideCreate):
    ride_type: RideType = RideType.TRUCK
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    max_insurance: str
    has_worker: bool


class RideUpdateFare(BaseModel):
    fare: int


class RideUpdateEndAddress(BaseModel):
    end_address: str


class RideUpdateStartAddress(BaseModel):
    start_address: str


class RideUpdateAlternativeEndAddress(BaseModel):
    alternative_end_address: str


class RideUpdateStopTime(BaseModel):
    stop_time: time


class RideCancel(BaseModel):
    canceller_id: int


class RideUseDiscount(BaseModel):
    discount_id: int


class RideAccept(BaseModel):
    driver_id: int


class ReviewCreate(BaseModel):
    ride_id: int
    user_id: int
    driver_id: int
    rating: int
    comment: str | None = None


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None


class PaymentCreate(BaseModel):
    user_id: int
    ride_id: int
    amount: int
    payment_method: PaymentMethod = PaymentMethod.CASH
    transaction_id: str | None = None


class PaymentUpdate(BaseModel):
    amount: int | None = None
    payment_method: PaymentMethod | None = None


class DWalletCreate(BaseModel):
    driver_id: int
    bank_account: str
    balance: int | None = 0


class DWalletUpdate(BaseModel):
    bank_account: str

class ChangeBalanceRequest(BaseModel):
    amount: int


class DriverCreate(BaseModel):
    na_code: int
    first_name: str
    last_name: str
    ce_code: int


class DriverUpdate(BaseModel):
    first_name: str
    last_name: str

class DiscountCreate(BaseModel):
    expire_time: datetime
    code: str
    percentage: float | None = None
    amount: int | None = None
    ride_type: DiscountType | None = DiscountType.ALL


class DiscountUpdate(BaseModel):
    expire_time: datetime | None = None
    percentage: float | None = None
    amount: int | None = None
    ride_type: DiscountType | None = None

class ComplaintCreate(BaseModel):
    driver_id: int
    user_id: int
    reasons: str


class ComplaintUpdate(BaseModel):
    reasons: str


class UserDiscountCreate(BaseModel):
    user_id: int
    discount_id: int


class UserDiscountUpdate(BaseModel):
    used: bool

