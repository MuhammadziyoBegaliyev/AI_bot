
from aiogram.fsm.state import StatesGroup, State

class LocationsFlow(StatesGroup):
    waiting_user_location = State()
