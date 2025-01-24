import io

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message

from ..api.perfume_backend import get_products_request_mock
from ..config import app_settings
from ..database import stores_table, products_table, file_storage
from ..keyboards.prod_keyboard import products_keyboard
from ..states.state import AddPhotoState

router = Router()


@router.message(Command("p"))
async def send_products_list_to_chat_handler(message: Message) -> None:
    store: dict = stores_table.get_store_data_from_chat_id(message.chat.id)
    products: list[dict] = get_products_request_mock(
        token=app_settings.perfume_backend_api_token,
        store_id=store["code"],
        count_items=store["prod_count"],
    )
    for product in products:
        await message.answer(
            text="Товар: {}".format(product["beautifulName"]),
            reply_markup=products_keyboard()
        )


@router.callback_query(F.data.startswith("prod"))
async def on_shelf_handler(call: CallbackQuery) -> None:
    call_data = call.data.split(".")
    store = stores_table.get_store_data_from_chat_id(call.message.chat.id)
    product = {
        "prod_id": call_data[-1],
        "prod_name": call.message.text.split(": ")[-1],
        "prod_avail": call_data[1] == "on_shelf",
        "prod_store_code": store["code"],
    }
    products_table.insert_product(product)
    await call.message.answer(
        "Товар: '{}' отмечен успешно.\nСтатус: {}".format(
            product["prod_name"],
            "есть на полке" if call_data[1] == "on_shelf" else "нет на полке",
        )
    )


@router.callback_query(F.data.startswith("add_photo"))
async def photo_addition_handler(call: CallbackQuery, state: FSMContext) -> None:
    product_id: str = call.data.split(":")[-1]
    product_name: str = call.message.text.split(": ")[-1]

    await state.set_state(AddPhotoState.product_id)
    await state.update_data(product_id=product_id)

    await call.message.answer(f"Загрузите фото товара: {product_name}")
    await state.set_state(AddPhotoState.upload_photo)


@router.message(AddPhotoState.upload_photo, F.photo)
async def get_photo_handler(message: Message, state: FSMContext) -> None:
    user_data: dict = await state.get_data()
    file_bytes: io.BytesIO = await message.bot.download(message.photo[-1])

    file_storage.upload_product_photo(file_bytes, product_id=user_data["product_id"])

    await message.answer("Фото загружено успешно!")
    await state.clear()
