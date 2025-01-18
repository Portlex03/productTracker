from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
# from schedulers import add_scheduler_jobs

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(f"chat.id: {message.chat.id}")


@router.my_chat_member()
async def group_addition_handler(message: Message) -> None:
    # add_scheduler_jobs(message)
    bot_name = await message.bot.get_my_name()
    await message.answer(f"Бот {bot_name.name} успешно добавлен в группу!")
