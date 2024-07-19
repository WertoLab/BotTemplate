from aiogram import Router, types
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import Paper
from handlers.filters import IsAllowedUser
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data.startswith('delete_paper:'))
async def delete_paper(callback_query: CallbackQuery):
    logging.info(f"Callback query received for delete_paper: {callback_query.data}")

    paper_id = int(callback_query.data.split(':')[1])
    session: Session = database.get_session()

    paper = session.query(Paper).filter(Paper.id == paper_id).first()
    logging.info(f"Paper to delete: {paper}")

    if not paper:
        await callback_query.message.answer("Работа не найдена.")
        await callback_query.answer()
        return

    session.delete(paper)
    session.commit()
    session.close()

    await callback_query.message.answer(f"Работа '{paper.title}' успешно удалена.")
    await callback_query.answer()
