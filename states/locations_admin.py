from aiogram.fsm.state import StatesGroup, State

class AddLocationFlow(StatesGroup):
    waiting_title = State()
    waiting_address = State()
    waiting_link = State()
    waiting_point = State()
