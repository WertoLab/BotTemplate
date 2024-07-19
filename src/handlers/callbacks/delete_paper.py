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
    paper_id = int(callback_query.data.split(':')[1])
    session: Session = database.get_session()
    paper = session.query(Paper).filter(Paper.id == paper_id).first()

    if paper:
        session.delete(paper)
        session.commit()
        await callback_query.message.answer(f"Работа '{paper.title}' была успешно удалена.")
    else:
        await callback_query.message.answer("Работа не найдена или уже была удалена.")

    session.close()
    await callback_query.answer()
