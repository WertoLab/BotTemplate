from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from handlers.filters import IsAllowedUser
from handlers.states import PaperState
from services import translate_text, gateway_service
from database.db import database
from database.models import User, Paper
from sqlalchemy.orm import Session
import asyncio
import logging

router = Router()

@router.message(IsAllowedUser())
async def handle_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == PaperState.waiting_for_title.state:
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
        session.close()

        await message.answer(f"Научная работа '{message.text}' сохранена с переводом '{translated_title}'.")

        try:
            similar_titles = await asyncio.wait_for(gateway_service.fetch_similar_titles(translated_title), timeout=200)
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
    else:
        await message.answer("Я не понимаю этот запрос. Пожалуйста, используйте команды или следуйте инструкциям.")
