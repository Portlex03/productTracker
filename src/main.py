import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

from backend_api_connector import get_products
from db_api_connector import StoresDBConnector, ProductsDBConnector

# Load environment variables
load_dotenv()

# Bot and API tokens
BOT_TOKEN: str = getenv("BOT_TOKEN")
PRODUCTS_API_TOKEN: str = getenv("PRODUCTS_API_TOKEN")

# Database connection parameters
DB_CONNECTION_PARAMS: tuple[str, str] = getenv("SUPABASE_URL"), getenv("SUPABASE_KEY")

# Initialize connectors
stores_db_connector = StoresDBConnector()
products_db_connector = ProductsDBConnector()

# Dispatcher
dp = Dispatcher()


def create_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Есть на полке", callback_data=f"on_shelf:{product_id}"),
         InlineKeyboardButton(text="Нет на полке", callback_data=f"off_shelf:{product_id}"),
         InlineKeyboardButton(text="Добавить фото", callback_data=f"add_photo:{product_id}")]
    ])
    return keyboard


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    store = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    await message.answer(
        "Бот подключился успешно!\nНаименование магазина: {}".format(
            store["store_name"]
        )
    )


@dp.message(Command("products"))
async def get_products_handler(message: Message) -> None:

    store: dict = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    products: list[dict] = get_products(
        token=PRODUCTS_API_TOKEN, store_id=store["store_id"], count_items=store["store_count_items"]
    )

    for product in products:
        product_name = product["beautifulName"]
        product_code = product["code"]  # Используем код продукта
        keyboard = create_product_keyboard(product_code)

        await message.answer(text=f"Товар: {product_name}", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("on_shelf"))
async def handle_on_shelf(call: CallbackQuery) -> None:
    product_id = call.data.split(":")[-1]  
    store: dict = stores_db_connector.get_store_data_from_chat_id(call.message.chat.id)
    store_id = store["store_id"] 

    try:
        products_db_connector.update_shelf_status(
            prod_id=product_id, prod_store_id=store_id, prod_avail=True
        )
        await call.answer("Товар отмечен как 'Есть на полке'.")
    except Exception as e:
        await call.answer(f"Ошибка обновления: {e}")

@dp.callback_query(F.data.startswith("off_shelf"))
async def handle_on_shelf(call: CallbackQuery) -> None:
    product_id = call.data.split(":")[-1]  
    store: dict = stores_db_connector.get_store_data_from_chat_id(call.message.chat.id)
    store_id = store["store_id"]  

    try:
        products_db_connector.update_shelf_status(
            prod_id=product_id, prod_store_id=store_id, prod_avail=False
        )
        await call.answer("Товар отмечен как 'Есть на полке'.")
    except Exception as e:
        await call.answer(f"Ошибка обновления: {e}")


async def main() -> None:

    bot = Bot(token=BOT_TOKEN)

    stores_db_connector.connect(*DB_CONNECTION_PARAMS)
    products_db_connector.connect(*DB_CONNECTION_PARAMS)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
