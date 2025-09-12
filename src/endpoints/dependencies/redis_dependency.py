from redis.asyncio import Redis
from ...service_layer.redis_client import RedisClient

redis_dependency = RedisClient()

def get_redis() -> Redis:
    return redis_dependency.redis
