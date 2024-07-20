from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.filters import IsAllowedUser
import logging

router = Router()


@router.callback_query(IsAllowedUser(), lambda c: c.data == 'help')
async def help(callback_query: CallbackQuery):
    logging.info(f"Callback query received for help")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    await callback_query.message.edit_text(
        "1. Отправить название научной работы и получить список похожих названий.\n"
        "2. Посмотреть список ваших сохраненных работ.\n"
        "Просто выберите соответствующую опцию в меню.",
        reply_markup=keyboard
    )

    await callback_query.answer()
