from aiogram import Bot, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..states.app_states import AppState
from .product_handlers import (
    delete_last_prod_list_handler,
    send_prod_list_to_chat_handler,
)

router = Router()

scheduler = AsyncIOScheduler()


@router.message(Command("run_prod_scheduler"))
async def run_prod_scheduler_handler(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.set_state(AppState.store_data)
    store_data: dict = await state.get_value("store_data")

    check_start_time = store_data["prod_check_time"]
    start_hour, start_minute, _ = map(int, check_start_time.split(":"))

    daily_checks_count = store_data["daily_checks_count"]
    daily_checks_interval = store_data["daily_checks_interval"]

    for i in range(daily_checks_count):
        call_hour = start_hour + i * daily_checks_interval

        scheduler.add_job(
            delete_last_prod_list_handler,
            "cron",
            args=(message, state, bot),
            hour=call_hour,
            minute=start_minute,
        )

        scheduler.add_job(
            send_prod_list_to_chat_handler,
            "cron",
            args=(message, state),
            hour=call_hour,
            minute=start_minute,
        )

    scheduler.start()

    await message.answer("Проверка товаров включена.")


@router.message(Command("stop_prod_scheduler"))
async def stop_prod_scheduler_handler(message: Message) -> None:
    scheduler.remove_all_jobs()
    scheduler.shutdown()

    await message.answer("Проверка товаров выключена.")
