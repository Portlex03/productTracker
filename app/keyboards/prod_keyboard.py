import uuid

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def products_keyboard() -> InlineKeyboardMarkup:
    prod_id = uuid.uuid4()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Есть на полке", callback_data=f"prod.on_shelf.{prod_id}"
                ),
                InlineKeyboardButton(
                    text="Нет на полке", callback_data=f"prod.off_shelf.{prod_id}"
                ),
                InlineKeyboardButton(
                    text="Добавить фото", callback_data=f"add_photo.{prod_id}"
                ),
            ]
        ]
    )
    return keyboard
