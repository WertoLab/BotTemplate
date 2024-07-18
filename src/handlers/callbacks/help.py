from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
import logging

router = Router()

@router.callback_query(lambda c: c.data == 'help')
async def help(callback_query: CallbackQuery):
    help_text = (
        "Я могу помочь вам в следующих задачах:\n"
        "1. Отправить название научной работы и получить список похожих названий.\n"
        "2. (В будущем) Посмотреть список ваших сохраненных работ.\n"
        "Просто выберите соответствующую опцию в меню."
    )
    try:
        await callback_query.answer(help_text)
    except TelegramBadRequest as e:
        if "query is too old and response timeout expired or query ID is invalid" in str(e):
            logging.warning("Callback query is too old or invalid")
        else:
            logging.error(f"Failed to answer callback query: {e}")
