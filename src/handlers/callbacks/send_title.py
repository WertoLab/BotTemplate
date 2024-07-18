from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from handlers.states import PaperState

router = Router()

@router.callback_query(lambda c: c.data == 'send_title')
async def send_title(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте название вашей научной работы.")
    await state.set_state(PaperState.waiting_for_title)
    await callback_query.answer()
