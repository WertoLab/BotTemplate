from aiogram import Router
from aiogram.types import CallbackQuery
from handlers.filters import IsAllowedUser
from keyboards.main_menu import get_main_menu
import logging

router = Router()


@router.callback_query(IsAllowedUser(), lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    logging.info(f"Callback query received for back_to_main")

    await callback_query.message.edit_text(
        f"Привет, {callback_query.from_user.username}!\n\n"
        "Я ИИ ассистент, который поможет вам в написании научных работ. Вы можете выбрать одну из опций в меню ниже.",
        reply_markup=get_main_menu()
    )

    await callback_query.answer()
