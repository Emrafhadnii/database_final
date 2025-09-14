from src.service_layer.redis_client import RedisClient

redis_dependency = RedisClient()


async def get_redis() -> RedisClient:
    return redis_dependency
