from pathlib import Path
from config import config
from database import database, redis_client
import sys


project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / 'src'))


token = config.TOKEN_BOT
print(f"Telegram Bot Token: {token}")

session = database.get_session()
print("PostgreSQL session created successfully.")

redis_client.set('key', 'value')
value = redis_client.get('key').decode('utf-8')
print(f"Value from Redis: {value}")

print("Configuration and database connections are set up successfully.")
