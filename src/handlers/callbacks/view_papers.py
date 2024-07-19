from aiogram import Router, types
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import User, Paper
from handlers.filters import IsAllowedUser
from keyboards import get_delete_paper_keyboard
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data == 'view_papers')
async def view_papers(callback_query: CallbackQuery):
    logging.info("Callback query received for view_papers")

    session: Session = database.get_session()
    user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    logging.info(f"User: {user}")

    if not user:
        await callback_query.message.answer("Вы не зарегистрированы в системе.")
        await callback_query.answer()
        return

    papers = session.query(Paper).filter(Paper.user_id == user.id).all()
    logging.info(f"Papers: {papers}")
    session.close()

    if not papers:
        await callback_query.message.answer("У вас нет сохраненных работ.")
        await callback_query.answer()
        return

    response_text = "Ваши сохраненные работы:\n\n"
    for paper in papers:
        response_text += f"- {paper.title} (Перевод: {paper.translated_title})\n"

    keyboard = get_delete_paper_keyboard(papers)
    logging.info(f"Keyboard: {keyboard.inline_keyboard}")

    messages = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]

    try:
        for msg in messages:
            await callback_query.message.answer(msg, reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

    await callback_query.answer()
