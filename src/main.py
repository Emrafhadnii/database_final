from contextlib import asynccontextmanager
from config.mongo_db import db
from fastapi import FastAPI
from .endpoints.dependencies.bus_dependency import messagebus
from .endpoints.dependencies.redis_dependency import redis_dependency
from .shared.mappings import mappers
from .endpoints import (
    users,
    vehicles,
    drivers,
    rides,
    discounts,
    dwallet,
    payments,
    reviews,
    complaints,
)

mappers()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_dependency.connect()
    await messagebus.connect()
    await db["complaint"].create_index(
        [("reasons", "text")], default_language="english"
    )
    await db["review"].create_index([("comment", "text")], default_language="english")

    yield

    await messagebus.channel.close()
    await messagebus.connection.close()
    await redis_dependency.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(vehicles.router, prefix="/api", tags=["vehicles"])
app.include_router(drivers.router, prefix="/api", tags=["drivers"])
app.include_router(rides.router, prefix="/api", tags=["rides"])
app.include_router(discounts.router, prefix="/api", tags=["discounts"])
app.include_router(dwallet.router, prefix="/api", tags=["dwallet"])
app.include_router(payments.router, prefix="/api", tags=["payments"])
app.include_router(reviews.router, prefix="/api", tags=["reviews"])
app.include_router(complaints.router, prefix="/api", tags=["complaints"])
