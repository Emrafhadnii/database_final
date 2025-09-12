from src.shared.abstract_enum import BaseEnum


class VehicleType(BaseEnum):
    CAR = "CAR"
    TRUCK = "TRUCK"
    MOTORCYCLE = "MOTORCYCLE"

class DiscountType(BaseEnum):
    ALL = "ALL"
    TAXI = "TAXI"
    TRUCK = "TRUCK"
    BOX = "BOX"

class PaymentMethod(BaseEnum):
    CREDIT_CARD = "CREDIT_CARD"
    CASH = "CASH"
    SNAP_WALLET = "SNAP_WALLET"

class RideType(BaseEnum):
    TAXI = "TAXI"
    BOX = "BOX"
    TRUCK = "TRUCK"

class RideStatus(BaseEnum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    IN_PROGRESS = "IN_PROGRESS"


class EntityType(BaseEnum):
    DRIVER = "drivers"
    COMPLAINT = "complaints"
    DISCOUNT = "discounts"
    DWALLET = "dwallet"
    PAYMENT = "payments"
    REVIEW = "reviews"
    RIDE = "rides"
    USER = "users"
    VEHICLE = "vehicles"
