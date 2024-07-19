from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить название", callback_data="send_title")],
        [InlineKeyboardButton(text="Посмотреть список сохраненных работ", callback_data="view_papers")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")]
    ])
    return keyboard
