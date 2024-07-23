from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from database.models import User, Paper
from database.db import database
from sqlalchemy.orm import Session
from handlers.filters import IsAllowedUser
from handlers.states import PaperState
from services import translate_text, gateway_service
import asyncio
import logging

router = Router()


@router.message(IsAllowedUser())
async def handle_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == PaperState.waiting_for_title.state:
        if len(message.text) > 255:
            await message.answer("Название работы слишком длинное. Пожалуйста, введите более короткое название.")
            return

        translated_title = await translate_text(message.text)

        if len(translated_title) > 255:
            await message.answer("Название работы слишком длинное. Пожалуйста, введите более короткое название.")
            return

        session: Session = database.get_session()

        try:
            user = session.query(User).filter(User.user_id == message.from_user.id).first()

            if not user:
                user = User(user_id=message.from_user.id, username=message.from_user.username)
                session.add(user)
                session.commit()

            paper = Paper(title=message.text, translated_title=translated_title, user_id=user.id)
            session.add(paper)
            session.commit()

            await message.answer(f"Ищу самую похожую по смыслу работу с ({message.text})")

            try:
                similar_titles = await asyncio.wait_for(gateway_service.fetch_similar_titles(translated_title),
                                                        timeout=200)
                if similar_titles:
                    similar_titles_text = "\n".join([f"{i + 1}. {title}" for i, title in enumerate(similar_titles)])
                    response_text = f"Вот список самых похожих названий, которые мы смогли найти:\n{similar_titles_text}"
                    await message.answer(response_text)
                else:
                    await message.answer("Не удалось найти похожих названий.")
            except asyncio.TimeoutError:
                logging.error("Timeout while fetching similar titles")
                await message.answer(
                    "Произошла ошибка при попытке получить похожие названия. Попробуйте еще раз позже.")

        except Exception as e:
            logging.error(f"Error handling text: {e}")
            await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз.")

        finally:
            database.close_session()

        await state.clear()
    else:
        await message.answer("Я не понимаю этот запрос. Пожалуйста, используйте команды или следуйте инструкциям.")
