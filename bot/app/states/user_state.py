from aiogram.fsm.state import StatesGroup, State

class UserAuth(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()