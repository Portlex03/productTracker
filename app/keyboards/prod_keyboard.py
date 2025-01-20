from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def products_keyboard(product_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Есть на полке", callback_data=f"on_shelf:{product_id}"),
                InlineKeyboardButton(text="Нет на полке", callback_data=f"off_shelf:{product_id}"),
                InlineKeyboardButton(text="Добавить фото", callback_data=f"add_photo:{product_id}"),
            ]
        ]
    )
    return keyboard
