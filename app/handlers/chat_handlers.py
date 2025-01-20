from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from ..database import stores_table

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    try:
        stores_table.get_store_data_from_chat_id(message.chat.id)
        message.answer("Бот запущен. Ваш чат успешно авторизован в базе данных!")
    except ValueError:
        # TODO: написать функцию выдачи временной регистрации
        await message.answer("Чат не зарегистрирован в базе данных. Вам была выдано временная регистрация.")


@router.my_chat_member()
async def group_addition_handler(message: Message) -> None:
    bot_name = await message.bot.get_my_name()
    await message.answer(f"Бот {bot_name.name} успешно добавлен в группу!")


@router.message(Command("get_chat_id"))
async def get_chat_id_handler(message: Message) -> None:
    await message.answer(f"Chat ID: {message.chat.id}")
