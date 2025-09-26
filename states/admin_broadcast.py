# path: states/admin_broadcast.py
from aiogram.fsm.state import StatesGroup, State

class AdminBroadcast(StatesGroup):
    choosing_mode = State()        # "promo" yoki "msg"
    ask_photo = State()            # rasm kerakmi?
    waiting_photo = State()        # rasm kutish
    waiting_text = State()         # matn kutish
    preview = State()              # preview/confirm
