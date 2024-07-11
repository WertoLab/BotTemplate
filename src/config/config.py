from pathlib import Path
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        dotenv_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path)

        self.TOKEN_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.REDIS_URL = os.getenv("REDIS_URL")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        self.WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
        self.WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT"))
        self.ALLOWED_USERS = list(map(int, os.getenv("ALLOWED_USERS").split(',')))

        print(f"Loaded TELEGRAM_BOT_TOKEN: {self.TOKEN_BOT}")
        print(f"Loaded DATABASE_URL: {self.DATABASE_URL}")
        print(f"Loaded REDIS_URL: {self.REDIS_URL}")
        print(f"Loaded WEBHOOK_URL: {self.WEBHOOK_URL}")
        print(f"Loaded ALLOWED_USERS: {self.ALLOWED_USERS}")


config = Config()
