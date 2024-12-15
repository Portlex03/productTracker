from aiogram.fsm.state import StatesGroup, State

class AddPhotoState(StatesGroup):
    product_id = State()
    upload_photo = State()
