from redis.asyncio import Redis
from config.settings import settings

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        self.redis = Redis(port=settings.REDIS_PORT,host=settings.REDIS_HOST,db=0,
                        password=None,decode_responses=True
                        )   
        
    async def disconnect(self):
        await self.redis.close()
