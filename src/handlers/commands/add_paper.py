from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.filters import IsAllowedUser
from handlers.states import PaperState

router = Router()

@router.message(Command("add_paper"), IsAllowedUser())
async def add_paper(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте название вашей научной работы.")
    await state.set_state(PaperState.waiting_for_title)
