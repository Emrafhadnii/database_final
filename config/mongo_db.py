from .settings import settings
from pymongo import AsyncMongoClient

mongo_url = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/?authSource=admin"

client = AsyncMongoClient(mongo_url)
db = client["mydatabase"]
