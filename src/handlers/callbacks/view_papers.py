from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
import logging

router = Router()


@router.callback_query(lambda c: c.data == 'view_papers')
async def view_papers(callback_query: CallbackQuery):
    try:
        message_text = "Функция просмотра списка сохраненных работ пока не реализована."
        messages = [message_text[i:i + 4096] for i in range(0, len(message_text), 4096)]

        for msg in messages:
            await callback_query.message.answer(msg)
    except TelegramBadRequest as e:
        if "query is too old and response timeout expired or query ID is invalid" in str(e):
            logging.warning("Callback query is too old or invalid")
        else:
            logging.error(f"Failed to answer callback query: {e}")

