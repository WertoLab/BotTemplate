from aiogram.fsm.state import StatesGroup, State

class PaperState(StatesGroup):
    waiting_for_title = State()
