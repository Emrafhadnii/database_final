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
    USER_DISCOUNT = "user_discounts"
    BOX_RIDE = "box_rides"
    TRUCK_RIDE = "truck_rides"
    TAXI_RIDE = "taxi_rides"


class BoxInsurance(BaseEnum):
    FIVE_MIL = "FIVE_MIL"
    TEN_MIL = "TEN_MIL"
    FIFTEEN_MIL = "FIFTEEN_MIL"
    THIRTY_MIL = "THIRTY_MIL"


class TruckInsurance(BaseEnum):
    FIVE_MIL = "FIVE_MIL"
    TEN_MIL = "TEN_MIL"
    FIFTEEN_MIL = "FIFTEEN_MIL"
    THIRTY_MIL = "THIRTY_MIL"
    FIFTY_MIL = "FIFTY_MIL"
    HUNDRED_MIL = "HUNDRED_MIL"


class ConsignmentType(BaseEnum):
    FOOD = "FOOD"
    CLOTHES = "CLOTHES"
    ELECTRICAL = "ELECTRICAL"
    COSMETICS = "COSMETICS"
    LETTER = "LETTER"
    OTHERS = "OTHERS"
