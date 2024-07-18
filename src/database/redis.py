import redis.asyncio as aioredis
from config import config
from redis.exceptions import RedisError

class RedisClient:
    def __init__(self):
        self._redis = None

    async def connect(self):
        try:
            self._redis = aioredis.from_url(config.REDIS_URL)
        except RedisError as e:
            print(f"Redis connection error: {e}")
            raise

    async def close(self):
        if self._redis:
            try:
                await self._redis.close()
            except RedisError as e:
                print(f"Redis close error: {e}")
            finally:
                self._redis = None

    def get_redis(self):
        return self._redis


redis_client = RedisClient()

async def setup_redis():
    await redis_client.connect()

async def shutdown_redis():
    await redis_client.close()
