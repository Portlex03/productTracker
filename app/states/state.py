from aiogram.fsm.state import State, StatesGroup


class AddPhotoState(StatesGroup):
    product_id = State()
    upload_photo = State()
