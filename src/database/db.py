from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config
from .models import init_db

class Database:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL, pool_size=20, max_overflow=0)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        init_db(self.engine)

    def get_session(self):
        return self.SessionLocal()

    def close_session(self):
        self.SessionLocal.remove()


database = Database()
