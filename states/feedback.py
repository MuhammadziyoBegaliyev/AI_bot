# path: states/feedback.py
from aiogram.fsm.state import StatesGroup, State
class FeedbackFlow(StatesGroup):
    waiting_text = State()
    waiting_complaint_text = State()
    waiting_complaint_photo = State()
    waiting_complaint_location = State()
