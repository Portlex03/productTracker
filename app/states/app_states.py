from aiogram.fsm.state import State, StatesGroup


class AppState(StatesGroup):
    chat_store = State()
    last_prod_list = State()


class AddPhotoState(StatesGroup):
    product_id = State()
    upload_photo = State()
