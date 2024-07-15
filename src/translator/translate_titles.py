from googletrans import Translator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Title, Base
from config import config


engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

translator = Translator()

file_path = config.TITLES_PATH

with open(file_path, 'r', encoding='utf-8') as file:
    titles = file.readlines()

for title in titles:
    title = title.strip()
    translated = translator.translate(title, dest='en').text

    new_title = Title(original_title=title, translated_title=translated)
    session.add(new_title)

session.commit()
session.close()
