from aiogram import Bot, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .product_handlers import (
    send_prod_list_to_chat_handler,
    delete_last_prod_list_handler,
)

router = Router()

scheduler = AsyncIOScheduler()


@router.message(Command("run_prod_scheduler"))
async def run_prod_scheduler_handler(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    trigger = IntervalTrigger(minutes=20)

    scheduler.add_job(
        delete_last_prod_list_handler, trigger, args=(message, state, bot)
    )
    scheduler.add_job(
        send_prod_list_to_chat_handler, trigger, args=(message, state)
    )

    scheduler.start()

    await message.answer("Проверка товаров включена.")


@router.message(Command("stop_prod_scheduler"))
async def stop_prod_scheduler_handler(message: Message) -> None:
    scheduler.remove_all_jobs()
    scheduler.shutdown()

    await message.answer("Проверка товаров выключена.")
