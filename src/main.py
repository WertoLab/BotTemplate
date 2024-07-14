import sys
import asyncio
from pathlib import Path
from config import config
from database import database, setup_redis, shutdown_redis, redis_client

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / 'src'))

token = config.TOKEN_BOT
print(f"Telegram Bot Token: {token}")

async def main():
    await setup_redis()

    session = database.get_session()
    print("PostgreSQL session created successfully.")

    redis = redis_client._redis
    await redis.set('key', 'value')
    value = await redis.get('key', encoding='utf-8')
    print(f"Value from Redis: {value}")

    print("Configuration and database connections are set up successfully.")

    await shutdown_redis()

if __name__ == '__main__':
    asyncio.run(main())
