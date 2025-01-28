from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from ..database import stores_table

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer("Бот запущен.")
    try:
        stores_table.get_store_data_from_chat_id(message.chat.id)
        await message.answer("Ваш чат успешно авторизован в базе данных!")
    except ValueError:
        stores_table.insert_store_with_temp_code(message.chat.id)
        await message.answer("Чат не зарегистрирован в базе данных. Вам была выдана временная регистрация.")
