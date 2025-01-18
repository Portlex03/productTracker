# from aiogram.types import Message
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# # from apscheduler.triggers.cron import CronTrigger

# from apscheduler.triggers.interval import IntervalTrigger

# from product_handlers import send_products_handler

# scheduler = AsyncIOScheduler()

# def add_scheduler_jobs(message: Message) -> None:
#     # trigger = CronTrigger(day_of_week='mon-fri', hour=10, minute=0)
#     trigger = IntervalTrigger(minutes=20)
#     scheduler.add_job(send_products_handler, trigger=trigger, args=(message,))
