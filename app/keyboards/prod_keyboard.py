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


def updated_products_keyboard(
    inline_kb: list[list[InlineKeyboardButton]], buttons_data2delete: list[str]
    ) -> InlineKeyboardMarkup:
    new_inline_kb = [
        [button for button in row if button.callback_data not in buttons_data2delete] for row in inline_kb
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=new_inline_kb)
    return keyboard
