from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.filters import IsAllowedUser
import logging
from keyboards import get_main_menu

router = Router()

@router.callback_query(IsAllowedUser(), lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    logging.info("Callback query received for back_to_main")

    main_text = (
        f"Привет, {callback_query.from_user.username}!\n\n"
        "Я ИИ ассистент, который поможет вам в написании научных работ. "
        "Вы можете выбрать одну из опций в меню ниже."
    )

    markup = get_main_menu()

    await callback_query.message.edit_text(main_text, reply_markup=markup)
    await callback_query.answer()
