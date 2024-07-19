from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session
from database.db import database
from database.models import User, Paper
from handlers.filters import IsAllowedUser
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data == 'view_papers')
async def view_papers(callback_query: CallbackQuery):
    logging.info(f"Callback query received for view_papers")

    session: Session = database.get_session()
    user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    papers = user.papers if user else []

    logging.info(f"User: {user}")
    logging.info(f"Papers: {papers}")

    if not papers:
        await callback_query.message.answer("У вас нет сохраненных работ.")
        await callback_query.answer()
        return

    buttons = []
    for paper in papers:
        buttons.append(
            [InlineKeyboardButton(
                text=f"{paper.title}",
                callback_data=f"delete_paper:{paper.id}"
            )]
        )
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer("Ваши работы:", reply_markup=markup)
    await callback_query.answer()
