import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db_api_connector import stores_db_connector, products_db_connector
from handlers import router

load_dotenv()

BOT_TOKEN: str = getenv("BOT_TOKEN")

DB_CONNECTION_PARAMS: tuple[str, str] = getenv("SUPABASE_URL"), getenv("SUPABASE_KEY")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=BOT_TOKEN)

    dp.include_router(router)

    stores_db_connector.connect(*DB_CONNECTION_PARAMS)
    products_db_connector.connect(*DB_CONNECTION_PARAMS)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
