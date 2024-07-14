import aioredis
import asyncio
from config import config

class RedisClient:
    def __init__(self):
        self._redis = None

    async def connect(self):
        self._redis = await aioredis.create_redis_pool(config.REDIS_URL)

    async def close(self):
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()
            self._redis = None

redis_client = RedisClient()

async def setup_redis():
    await redis_client.connect()

async def shutdown_redis():
    await redis_client.close()
