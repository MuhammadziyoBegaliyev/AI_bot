# path: states/search.py
from aiogram.fsm.state import StatesGroup, State
class SearchFlow(StatesGroup):
    waiting_query = State()
