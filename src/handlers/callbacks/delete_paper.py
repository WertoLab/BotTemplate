from aiogram import Router, types
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import Paper
from handlers.filters import IsAllowedUser
from keyboards import create_delete_keyboard
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data.startswith('delete_paper_'))
async def delete_paper(callback_query: CallbackQuery):
    logging.info(f"Callback query received for delete_paper")

    paper_id = int(callback_query.data.split('_')[2])
    session: Session = database.get_session()

    try:
        paper = session.query(Paper).filter(Paper.id == paper_id).first()
        if paper:
            session.delete(paper)
            session.commit()
            await callback_query.message.edit_text("Работа успешно удалена.")
        else:
            await callback_query.message.edit_text("Работа не найдена.")

        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error deleting paper: {e}")
        await callback_query.message.edit_text("Произошла ошибка при удалении работы.")
    finally:
        database.close_session()
