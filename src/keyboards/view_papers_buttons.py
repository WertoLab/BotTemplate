from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_papers_keyboard(papers):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if papers:
        for paper in papers:
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(
                    text=f"Выбрать: {paper.title}",
                    callback_data=f"select_paper_{paper.id}"
                )]
            )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="НаФзад", callback_data="back_to_main")]
    )

    return keyboard

def create_delete_keyboard(paper_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_paper_{paper_id}")],
        [InlineKeyboardButton(text="Назад", callback_data="view_papers")]
    ])
    return keyboard
