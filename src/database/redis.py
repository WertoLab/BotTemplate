import redis
from config import config

redis_client = redis.StrictRedis.from_url(config.REDIS_URL)
