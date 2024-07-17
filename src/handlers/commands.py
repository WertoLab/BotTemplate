from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import Session
from database.models import User, Paper
from database.db import database
from handlers.filters import IsAllowedUser
from googletrans import Translator
from pydantic import BaseModel
from config import config
from gateway.gateway_service import gateway_service
import logging
import asyncio

router = Router()

translator = Translator()

class SimilarTitleResponse(BaseModel):
    similar_title: str

class PaperState(StatesGroup):
    waiting_for_title = State()

async def translate_text(text, dest_language='en'):
    translated = translator.translate(text, dest=dest_language)
    return translated.text

@router.message(Command("start"))
async def start(message: types.Message):
    username = message.from_user.username
    greeting_text = (
        f"Привет, {username}!\n\n"
        "Я ИИ ассистент, который поможет вам в написании научных работ. "
        "Вы можете ввести название вашей работы, и я сохраню её для вас."
    )
    await message.answer(greeting_text)

@router.message(Command("add_paper"), IsAllowedUser())
async def add_paper(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте название вашей научной работы.")
    await state.set_state(PaperState.waiting_for_title)

@router.message(PaperState.waiting_for_title, IsAllowedUser())
async def save_paper(message: types.Message, state: FSMContext):
    logging.info(f"save_paper called with message: {message.text}")
    session: Session = database.get_session()
    user = session.query(User).filter(User.user_id == message.from_user.id).first()

    if not user:
        user = User(user_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()

    translated_title = await translate_text(message.text)

    paper = Paper(title=message.text, translated_title=translated_title, user_id=user.id)
    session.add(paper)
    session.commit()
    logging.info(f"Paper saved with title: {message.text} and translated title: {translated_title}")
    session.close()

    await message.answer(f"Научная работа '{message.text}' сохранена с переводом '{translated_title}'.")

    try:
        # Установка таймаута для запроса к внешнему сервису
        similar_titles = await asyncio.wait_for(gateway_service.fetch_similar_titles(translated_title), timeout=10.0)
        logging.info(f"Fetched similar titles: {similar_titles}")

        if similar_titles:
            similar_titles_text = "\n".join(similar_titles)
            response_text = f"Вот список самых похожих названий, которые мы смогли найти:\n{similar_titles_text}"
            await message.answer(response_text)
        else:
            await message.answer("Не удалось найти похожих названий.")

    except asyncio.TimeoutError:
        logging.error("Timeout while fetching similar titles")
        await message.answer("Произошла ошибка при попытке получить похожие названия. Попробуйте еще раз позже.")

    await state.clear()
