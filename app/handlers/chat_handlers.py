from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..database import stores_table
from ..states.app_states import AppState

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext) -> None:
    try:
        store_data = stores_table.get_store_data_from_chat_id(message.chat.id)
        message_text = "Бот запущен и готов к работе, ваш чат авторизован"
    except ValueError:
        store_data = stores_table.insert_store_with_temp_code(message.chat.id)
        message_text = "Бот запущен и готов к работе, ваш чат временно авторизован"

    await state.set_state(AppState.store_data)
    await state.update_data(store_data=store_data)

    await message.answer(message_text)
