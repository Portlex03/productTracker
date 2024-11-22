# TODO: изменить store_chat_id магазина с параметром store_id = 8 на верный
# TODO: удалить магазины Marafett из store_table и сделать type(store_id) = int вместо str
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from backend_api_connector import get_products
from db_api_connector import StoresDBConnector

load_dotenv()

BOT_TOKEN: str = getenv("BOT_TOKEN")

PRODUCTS_API_TOKEN: str = getenv("PRODUCTS_API_TOKEN")

DB_CONNECTION_PARAMS: tuple[str, str] = getenv("SUPABASE_URL"), getenv("SUPABASE_KEY")

dp = Dispatcher()

stores_db_connector = StoresDBConnector()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    store = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    await message.answer(
        "Бот подключился успешно!\nНаименование магазина: {}".format(
            store["store_name"]
        )
    )


@dp.message(Command("products"))
async def get_products_handler(message: Message, count_items: int) -> None:
    store: dict = stores_db_connector.get_store_data_from_chat_id(message.chat.id)
    products: list[dict] = get_products(
        token=PRODUCTS_API_TOKEN, store_id=store["store_id"], count_items=count_items
    )
    await ...

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    stores_db_connector.connect(*DB_CONNECTION_PARAMS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
