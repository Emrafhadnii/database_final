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
    user_discounts,
)

from src.event_handlers.mongo_sync_handlers import (
    handle_complaint_created,
    handle_review_created,
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
    await messagebus.subscribe("complaint_created", handle_complaint_created)
    await messagebus.subscribe("review_created", handle_review_created)

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
app.include_router(user_discounts.router, prefix="/api", tags=["user_discounts"])
