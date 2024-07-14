from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import config
from .models import init_db

class Database:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        init_db(self.engine)

    def get_session(self):
        return self.SessionLocal()


database = Database()
