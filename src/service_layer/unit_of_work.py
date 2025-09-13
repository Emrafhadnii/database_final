from config.postgres import SessionLocal
from src.repositories.complaints_repository import ComplaintSqlalchemyRepository
from src.repositories.discounts_repository import DiscountSqlalchemyRepository
from src.repositories.drivers_repository import DriverSqlalchemyRepository
from src.repositories.dwallet_repository import DWalletSqlalchemyRepository
from src.repositories.payments_repository import PaymentSqlalchemyRepository
from src.repositories.reviews_repository import ReviewSqlalchemyRepository
from src.repositories.rides_repository import RideSqlalchemyRepository
from src.repositories.users_repository import UserSqlalchemyRepository
from src.repositories.vehicles_repository import VehicleSqlalchemyRepository
from src.repositories.user_discounts_repository import UserDiscountSqlalchemyRepository


class UnitOfWork:
    def __init__(self):
        self.session = SessionLocal()
        self.complaint = ComplaintSqlalchemyRepository(self.session)
        self.discount = DiscountSqlalchemyRepository(self.session)
        self.driver = DriverSqlalchemyRepository(self.session)
        self.dwallet = DWalletSqlalchemyRepository(self.session)
        self.payment = PaymentSqlalchemyRepository(self.session)
        self.review = ReviewSqlalchemyRepository(self.session)
        self.ride = RideSqlalchemyRepository(self.session)
        self.user = UserSqlalchemyRepository(self.session)
        self.vehicle = VehicleSqlalchemyRepository(self.session)
        self.user_discount = UserDiscountSqlalchemyRepository(self.session)
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()
