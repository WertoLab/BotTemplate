import os
import asyncio
import aiohttp
import logging
from googletrans import Translator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Title, Base
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

translator = Translator()

file_path = config.TITLES_PATH


with open(file_path, 'r', encoding='utf-8') as file:
    titles = [title.strip() for title in file.readlines()]

async def translate_and_save(session, title):
    try:
        translated = translator.translate(title, dest='en').text
        new_title = Title(original_title=title, translated_title=translated)
        session.add(new_title)
        logger.info(f"Translated: {title} -> {translated}")
    except Exception as e:
        logger.error(f"Error translating '{title}': {e}")

async def main():
    tasks = []
    for title in titles:

        task = asyncio.create_task(translate_and_save(session, title))
        tasks.append(task)
        await asyncio.sleep(1)

    await asyncio.gather(*tasks)
    session.commit()
    session.close()

if __name__ == "__main__":
    asyncio.run(main())
