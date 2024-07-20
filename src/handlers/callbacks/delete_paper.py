from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from database.db import database
from database.models import Paper, User
from handlers.filters import IsAllowedUser
from keyboards import create_papers_keyboard
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

            user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
            papers = user.papers if user else []

            papers_list = "\n".join([f"{i+1}. {paper.title}" for i, paper in enumerate(papers)])
            message_text = f"Ваши сохраненные работы:\n\n{papers_list}\n\nВыберите работу для дальнейшего взаимодействия." if papers else "У вас нет сохраненных работ."
            keyboard = create_papers_keyboard(papers)

            await callback_query.message.edit_text(message_text, reply_markup=keyboard)
        else:
            await callback_query.message.edit_text("Работа не найдена.", reply_markup=create_papers_keyboard([]))

        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error deleting paper: {e}")
        await callback_query.message.edit_text("Произошла ошибка при удалении работы.")
    finally:
        database.close_session()
