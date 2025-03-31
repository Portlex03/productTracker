from aiogram.fsm.state import State, StatesGroup


class AppState(StatesGroup):
    store_data = State()
    last_prod_list = State()
