import io
from os import getenv

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from backend_api_connector import get_products
from storage_connector import storage_connector
from db_api_connector import products_db_connector, stores_db_connector
from keyboards import create_product_keyboard
from states import AddPhotoState

load_dotenv()

PRODUCTS_API_TOKEN: str = getenv("PRODUCTS_API_TOKEN")

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    store = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    await message.answer(
        "Бот подключился успешно!\nНаименование магазина: {}".format(
            store["store_name"]
        )
    )


@router.message(Command("products"))
async def get_products_handler(message: Message) -> None:
    store: dict = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    products: list[dict] = get_products(
        token=PRODUCTS_API_TOKEN,
        store_id=store["store_id"],
        count_items=store["store_count_items"],
    )

    for product in products:
        product_name = product["beautifulName"]
        product_code = product["code"]
        keyboard = create_product_keyboard(product_code)

        await message.answer(text=f"Товар: {product_name}", reply_markup=keyboard)


@router.callback_query(F.data.startswith("on_shelf"))
async def on_shelf_handler(call: CallbackQuery) -> None:
    product_id = call.data.split(":")[-1]
    store = stores_db_connector.get_store_data_from_chat_id(call.message.chat.id)
    store_id = store["store_id"]

    products_db_connector.insert_shelf_status(
        prod_id=product_id, prod_store_id=store_id, prod_avail=True
    )
    await call.answer("Информация о товаре записана: 'Есть на полке'.")


@router.callback_query(F.data.startswith("off_shelf"))
async def off_shelf_handler(call: CallbackQuery) -> None:
    product_id = call.data.split(":")[-1]
    store = stores_db_connector.get_store_data_from_chat_id(call.message.chat.id)
    store_id = store["store_id"]

    products_db_connector.insert_shelf_status(
        prod_id=product_id, prod_store_id=store_id, prod_avail=False
    )
    await call.answer("Информация о товаре записана: 'Нет на полке'.")


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

    storage_connector.upload_product_photo(
        file_bytes, product_id=user_data["product_id"]
    )

    await message.answer("Фото загружено успешно!")
    await state.clear()
