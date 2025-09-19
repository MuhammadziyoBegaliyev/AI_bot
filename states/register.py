# path: states/register.py
from aiogram.fsm.state import StatesGroup, State
class Register(StatesGroup):
    waiting_name = State()
    waiting_contact = State()
    waiting_age = State()
