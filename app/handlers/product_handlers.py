import time

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message

from ..api.perfume_backend import get_products_request
from ..config import app_settings
from ..database import stores_table, products_table
from ..keyboards.prod_keyboard import products_keyboard

from ..states.app_states import AppState

router = Router()


@router.message(Command("p"))
async def send_prod_list_to_chat_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AppState.chat_store)
    chat_store: dict = await state.get_value("chat_store")

    products: list[dict] = get_products_request(
        token=app_settings.perfume_backend_api_token,
        store_id=chat_store["code"],
        count_items=chat_store["prod_count"],
    )

    last_prod_list = []
    for product in products:
        sent_message = await message.answer(
            text="Товар: {}".format(product["beautifulName"]),
            reply_markup=products_keyboard(),
        )
        last_prod_list.append(sent_message.message_id)
        time.sleep(1)

    await state.update_data(last_prod_list=last_prod_list)


@router.message(Command("d"))
async def delete_last_prod_list_handler(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.set_state(AppState.last_prod_list)

    last_prod_list = await state.get_value("last_prod_list", None)

    if not last_prod_list:
        return None
    # TODO: add products in db as not detected on shelf
    await bot.delete_messages(chat_id=message.chat.id, message_ids=last_prod_list)


@router.callback_query(F.data.startswith("prod"))
async def on_shelf_handler(call: CallbackQuery, bot: Bot) -> None:
    _, prod_avail, prod_id = call.data.split(".")
    prod_avail = True if prod_avail == "on_shelf" else False

    store = stores_table.get_store_data_from_chat_id(call.message.chat.id)
    product = {
        "prod_id": prod_id,
        "prod_name": call.message.text.split(": ")[-1],
        "prod_avail": prod_avail,
        "prod_store_code": store["code"],
        "prod_employee_name": call.from_user.full_name,
    }
    products_table.insert_product(product)

    prod_status = "Есть на полке" if prod_avail else "Нет на полке"
    await call.answer(
        "Товар '{}' отмечен успешно.\nСтатус: {}".format(
            product["prod_name"], prod_status
        )
    )

    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
