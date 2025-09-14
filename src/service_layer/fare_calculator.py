from src.models.rides import Ride
from src.models.discounts import Discount
from src.models.enums import RideType
from geopy.distance import geodesic
from datetime import time


class FareCalculator:
    @staticmethod
    def calculate_fare(
        start_address: str,
        end_address: str,
        ride_type: RideType,
        alternative_end_address: str | None = None,
        stop_time: time | None = None,
        discount: Discount | None = None,
    ) -> int:
        if ride_type != RideType.TAXI:
            return 0

        distance = geodesic(start_address, end_address).kilometers
        fare = distance * 10000

        if alternative_end_address:
            second_distance = geodesic(end_address, alternative_end_address).kilometers
            fare += second_distance * 20000

        if stop_time:
            fare += (stop_time.minute / 5) * 5000

        if discount:
            if discount.percentage:
                fare -= fare * discount.percentage
            elif discount.amount:
                fare -= discount.amount

        return fare
