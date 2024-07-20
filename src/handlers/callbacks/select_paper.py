from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import Paper
from handlers.filters import IsAllowedUser
from keyboards import create_delete_keyboard, create_papers_keyboard
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data.startswith('select_paper_'))
async def select_paper(callback_query: CallbackQuery):
    logging.info(f"Callback query received for select_paper")

    paper_id = int(callback_query.data.split('_')[2])
    session: Session = database.get_session()

    try:
        paper = session.query(Paper).filter(Paper.id == paper_id).first()

        if paper:
            keyboard = create_delete_keyboard(paper_id)
            await callback_query.message.edit_text(
                f"Вы выбрали работу: {paper.title}",
                reply_markup=keyboard
            )
        else:
            await callback_query.message.edit_text("Работа не найдена.", reply_markup=create_papers_keyboard([]))

        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error selecting paper: {e}")
        await callback_query.message.edit_text("Произошла ошибка при выборе работы.")
    finally:
        database.close_session()
