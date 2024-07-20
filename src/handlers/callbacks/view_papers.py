from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import User
from handlers.filters import IsAllowedUser
from keyboards import create_papers_keyboard
import logging

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data == 'view_papers')
async def view_papers(callback_query: CallbackQuery):
    logging.info(f"Callback query received for view_papers")

    session: Session = database.get_session()

    try:
        user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()

        if user:
            papers = user.papers
            papers_list = "\n".join([f"{i+1}. {paper.title}" for i, paper in enumerate(papers)])
            message_text = f"Ваши сохраненные работы:\n\n{papers_list}\n\nВыберите работу для дальнейшего взаимодействия." if papers else "У вас нет сохраненных работ."
            keyboard = create_papers_keyboard(papers)
            await callback_query.message.edit_text(message_text, reply_markup=keyboard)
        else:
            keyboard = create_papers_keyboard([])
            await callback_query.message.edit_text("Вы не зарегистрированы.", reply_markup=keyboard)

        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error viewing papers: {e}")
        await callback_query.message.edit_text("Произошла ошибка при просмотре работ.")
    finally:
        database.close_session()
