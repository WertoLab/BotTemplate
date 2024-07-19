from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Отправить название", callback_data="send_title"))
    keyboard.add(InlineKeyboardButton(text="Посмотреть список сохраненных работ", callback_data="view_papers"))
    keyboard.add(InlineKeyboardButton(text="Помощь", callback_data="help"))
    return keyboard
