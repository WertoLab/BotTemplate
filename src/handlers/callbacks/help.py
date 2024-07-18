from aiogram import Router, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == 'help')
async def help(callback_query: CallbackQuery):
    help_text = (
        "Я могу помочь вам в следующих задачах:\n"
        "1. Отправить название научной работы и получить список похожих названий.\n"
        "2. (В будущем) Посмотреть список ваших сохраненных работ.\n"
        "Просто выберите соответствующую опцию в меню."
    )
    await callback_query.message.answer(help_text)
    await callback_query.answer()
