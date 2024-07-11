from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import Session
from database.models import User, Paper
from database.db import database
from handlers.filters import IsAllowedUser

router = Router()

class PaperState(StatesGroup):
    waiting_for_title = State()

@router.message(Command("start"))
async def start(message: types.Message):
    username = message.from_user.username
    greeting_text = (
        f"Привет, {username}!\n\n"
        "Я ИИ ассистент, который поможет вам в написании научных работ. "
        "Вы можете ввести название вашей работы, и я сохраню её для вас."
    )
    await message.answer(greeting_text)

@router.message(Command("add_paper"), IsAllowedUser())
async def add_paper(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте название вашей научной работы.")
    await state.set_state(PaperState.waiting_for_title)

@router.message(PaperState.waiting_for_title, IsAllowedUser())
async def save_paper(message: types.Message, state: FSMContext):
    session: Session = database.get_session()
    user = session.query(User).filter(User.user_id == message.from_user.id).first()

    if not user:
        user = User(user_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()

    paper = Paper(title=message.text, user_id=user.id)
    session.add(paper)
    session.commit()
    session.close()

    await message.answer(f"Научная работа '{message.text}' сохранена.")
    await state.clear()
