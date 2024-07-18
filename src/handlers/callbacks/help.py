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

    # Разделение текста на части, если он слишком длинный
    messages = [help_text[i:i + 4096] for i in range(0, len(help_text), 4096)]

    try:
        for msg in messages:
            await callback_query.message.answer(msg)
    except TelegramBadRequest as e:
        logging.error(f"Failed to send message: {e}")

