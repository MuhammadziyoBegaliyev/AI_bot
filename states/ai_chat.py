# path: states/ai.py
from aiogram.fsm.state import StatesGroup, State
class AIChat(StatesGroup):
    chatting = State()
