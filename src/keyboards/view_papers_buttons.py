from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_papers_keyboard(papers):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if papers:
        for paper in papers:
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(
                    text=f"{paper.title}",
                    callback_data=f"select_paper_{paper.id}"
                )]
            )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    )

    return keyboard
