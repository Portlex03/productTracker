from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def products_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Есть на полке", callback_data="kb.prod_avail.true"),
                InlineKeyboardButton(text="Нет на полке", callback_data="kb.prod_avail.false"),
            ]
        ]
    )
    return keyboard
