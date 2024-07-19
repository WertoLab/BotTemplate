from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_delete_paper_keyboard(papers):
    keyboard = InlineKeyboardMarkup()
    for paper in papers:
        keyboard.add(
            InlineKeyboardButton(f"Удалить '{paper.title}'", callback_data=f"delete_paper:{paper.id}")
        )
    return keyboard
