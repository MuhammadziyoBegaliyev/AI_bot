# path: states/admin.py
from aiogram.fsm.state import StatesGroup, State

class AdminDrug(StatesGroup):
    name = State(); uses = State(); side = State(); dosage = State()
    price_min = State(); price_max = State(); call_center = State(); alternatives = State()

class AdminPharmacy(StatesGroup):
    title = State(); lat = State(); lon = State(); address = State(); phone = State()

class AdminDelete(StatesGroup):
    drug_id = State(); pharmacy_id = State()
