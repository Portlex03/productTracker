import io
import os
from uuid import uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
import dotenv

from ..api.perfume_backend import get_products_request
from ..database import stores_table, products_table, storage_table
from ..keyboards.prod_keyboard import products_keyboard
from ..states.state import AddPhotoState

dotenv.load_dotenv()

PRODUCTS_API_TOKEN: str = os.getenv("PRODUCTS_API_TOKEN")

router = Router()


@router.message(Command("p"))
async def sssend_products_handler(message: Message) -> None:
    store: dict = stores_table.get_store_data_from_chat_id(message.chat.id)
    products: list[dict] = get_products_request(
        token=PRODUCTS_API_TOKEN,
        store_id=int(store["code"]),
        count_items=3,
    )

    for product in products:
        prod_id = uuid4()
        prod_name = product["beautifulName"]
        keyboard = products_keyboard(prod_id)

        await message.answer(text=f"Товар: {prod_name}", reply_markup=keyboard)


@router.callback_query(F.data.startswith("on_shelf"))
async def on_shelf_handler(call: CallbackQuery) -> None:
    prod_id = call.data.split(":")[-1]
    prod_name = call.message.text.split(": ")[-1]
    store = stores_table.get_store_data_from_chat_id(call.message.chat.id)
    store_code = store["code"]

    products_table.insert_product(
        prod_id=prod_id, prod_name=prod_name, prod_avail=True, prod_store_code=store_code
    )
    await call.message.answer(f"Товар: {prod_name}.\nОтметка: Есть на полке")


@router.callback_query(F.data.startswith("off_shelf"))
async def off_shelf_handler(call: CallbackQuery) -> None:
    prod_id = call.data.split(":")[-1]
    prod_name = call.message.text.split(": ")[-1]
    store = stores_table.get_store_data_from_chat_id(call.message.chat.id)
    store_code = store["code"]

    products_table.insert_product(
        prod_id=prod_id, prod_name=prod_name, prod_avail=False, prod_store_code=store_code
    )
    await call.message.answer(f"Товар: {prod_name}.\nОтметка: Нет на полке")


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

    storage_table.upload_product_photo(
        file_bytes, product_id=user_data["product_id"]
    )

    await message.answer("Фото загружено успешно!")
    await state.clear()
