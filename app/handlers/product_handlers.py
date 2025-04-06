import time

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message

from ..api.perfume_backend import get_products_request
from ..config import app_settings
from ..database import products_available_table, products_table
from ..keyboards.prod_keyboard import products_keyboard

from ..states.app_states import AppState

router = Router()


@router.message(Command("p"))
async def send_prod_list_to_chat_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(AppState.store_data)
    store_data: dict = await state.get_value("store_data")

    prod_count = store_data["prod_count"]
    products: list[dict] = get_products_request(
        token=app_settings.perfume_backend_api_token,
        store_id=store_data["code"],
        count_items=prod_count,
    )

    products_table.insert_products(products)

    last_prod_list = []
    for i, product in enumerate(products):
        try:
            sent_message = await message.answer_photo(
                photo=product["photo"],
                caption="Товар [{}/{}]: {}".format(
                    i + 1, prod_count, product["beautifulName"]
                ),
                reply_markup=products_keyboard(),
            )
        except TelegramBadRequest:
            sent_message = await message.answer(
                text="Товар [{}/{}]: {}".format(
                    i + 1, prod_count, product["beautifulName"]
                ),
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


@router.callback_query(F.data.startswith("kb.prod_avail"))
async def on_shelf_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    call_text = call.message.text or call.message.caption
    prod_num, prod_name = call_text.split(": ")
    prod_id = products_table.get_product_id_by_name(prod_name)
    prod_avail = True if call.data.split(".")[-1] == "true" else False

    await state.set_state(AppState.store_data)
    store_data: dict = await state.get_value("store_data")

    product = {
        "prod_id": prod_id,
        "prod_avail": prod_avail,
        "prod_store_id": store_data["id"],
        "prod_employee_id": call.from_user.id,
    }
    products_available_table.insert_product_avail(product)

    prod_status = "Есть на полке" if prod_avail else "Нет на полке"
    message = "{}: '{}' отмечен успешно.\nСтатус: {}"
    await call.answer(message.format(prod_num, prod_name, prod_status))

    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
