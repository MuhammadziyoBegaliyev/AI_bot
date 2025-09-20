# path: states/feedback.py
from aiogram.fsm.state import StatesGroup, State

class FeedbackFlow(StatesGroup):
    choosing_type = State()       # "Fikr"mi yoki "Shikoyat"mi
    rating_wait = State()         # 1..5 yulduz
    review_text = State()         # fikr matni (bahodan keyin)
    complaint_text = State()      # shikoyat matni
    complaint_add = State()       # rasm/lokatsiya/jo'natish bosqichi
    waiting_photo = State()       # "Rasm yuborish" bosilganda
    waiting_location = State()    # "Lokatsiyani yuborish" bosilganda
