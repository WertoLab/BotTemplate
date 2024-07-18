from aiogram import Router, types
from aiogram.filters import Command
from keyboards import get_main_menu

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    username = message.from_user.username
    greeting_text = (
        f"Привет, {username}!\n\n"
        "Я ИИ ассистент, который поможет вам в написании научных работ. "
        "Вы можете выбрать одну из опций в меню ниже."
    )
    await message.answer(greeting_text, reply_markup=get_main_menu())
