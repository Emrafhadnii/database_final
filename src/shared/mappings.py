from src.models.users import User, users_data_model
from src.models.vehicles import Vehicle, vehicles_data_model
from src.models.discounts import Discount, discounts_data_model
from src.models.drivers import Driver, drivers_data_model
from src.models.dwallet import DWallet, dwallet_data_model
from src.models.payments import Payment, payments_data_model
from src.models.reviews import Review, reviews_data_model
from src.models.rides import Ride, rides_data_model
from src.models.complaints import Complaint, complaints_data_model
from src.models.user_discounts import UserDiscount, user_discounts_data_model
from config.postgres import mapper_registry


def mappers():
    mapper_registry.map_imperatively(User, users_data_model)
    mapper_registry.map_imperatively(Vehicle, vehicles_data_model)
    mapper_registry.map_imperatively(Discount, discounts_data_model)
    mapper_registry.map_imperatively(Driver, drivers_data_model)
    mapper_registry.map_imperatively(DWallet, dwallet_data_model)
    mapper_registry.map_imperatively(Payment, payments_data_model)
    mapper_registry.map_imperatively(Review, reviews_data_model)
    mapper_registry.map_imperatively(Ride, rides_data_model)
    mapper_registry.map_imperatively(Complaint, complaints_data_model)
    mapper_registry.map_imperatively(UserDiscount, user_discounts_data_model)
