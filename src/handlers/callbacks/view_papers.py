from aiogram import Router, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == 'view_papers')
async def view_papers(callback_query: CallbackQuery):
    await callback_query.message.answer("Функция просмотра списка сохраненных работ пока не реализована.")
    await callback_query.answer()
