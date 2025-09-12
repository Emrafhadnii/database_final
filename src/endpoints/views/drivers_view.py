from src.service_layer.unit_of_work import UnitOfWork
from src.models.drivers import Driver


async def get_all_drivers(uow: UnitOfWork):
    async with uow:
        drivers = await uow.driver.select_all(Driver)
        return [driver.to_dict() for driver in drivers]


async def get_driver_by_id(driver_id: int, uow: UnitOfWork):
    async with uow:
        driver = await uow.driver.select_by_id(Driver, driver_id)
        if driver:
            return driver.to_dict()
        return None
