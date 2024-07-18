from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="Отправить название", callback_data="send_title")],
        [InlineKeyboardButton(text="Посмотреть список сохраненных работ", callback_data="view_papers")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
