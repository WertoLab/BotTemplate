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

    if user:
        papers = user.papers
        if papers:
            keyboard = InlineKeyboardMarkup()
            for paper in papers:
                keyboard.add(InlineKeyboardButton(
                    text=f"Удалить: {paper.title}", callback_data=f"delete_paper_{paper.id}")
                )
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
            await callback_query.message.edit_text(
                "Ваши сохраненные работы:",
                reply_markup=keyboard
            )
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
            ])
            await callback_query.message.edit_text("У вас нет сохраненных работ.", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ])
        await callback_query.message.edit_text("Вы не зарегистрированы.", reply_markup=keyboard)

    await callback_query.answer()
