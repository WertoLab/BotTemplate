from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_delete_paper_keyboard(papers):
    buttons = [
        [InlineKeyboardButton(f"Удалить '{paper.title}'", callback_data=f"delete_paper:{paper.id}")]
        for paper in papers
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
