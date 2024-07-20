from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_delete_keyboard(paper_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_paper_{paper_id}")],
        [InlineKeyboardButton(text="Назад", callback_data="view_papers")]
    ])
    return keyboard
