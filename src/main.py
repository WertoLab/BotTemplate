import sys
import asyncio
from pathlib import Path
from database import database, setup_redis, shutdown_redis, redis_client

project_root = Path(__file__).parent
sys.path.append(str(project_root / 'src'))

async def main():
    await setup_redis()

    session = database.get_session()
    try:
        print("PostgreSQL session создана успешно.")

    except Exception as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")
    finally:
        database.close_session()

    redis = redis_client.get_redis()
    try:
        await redis.set('key', 'value')
        value = await redis.get('key', encoding='utf-8')
        print(f"Значение из Redis: {value}")
    except Exception as e:
        print(f"Ошибка при работе с Redis: {e}")

    print("Настройка конфигурации и подключений к базе данных выполнена успешно.")

    await shutdown_redis()

if __name__ == '__main__':
    asyncio.run(main())
