import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import AppSettings
from database import connect2db_from_settings
from handlers import routers

app_settings = AppSettings()


async def main() -> None:
    bot = Bot(token=app_settings.bot_token)

    dp = Dispatcher()
    dp.include_routers(*routers)

    connect2db_from_settings(app_settings)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
