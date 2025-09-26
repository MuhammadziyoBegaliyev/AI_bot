# path: states/admin.py
from aiogram.fsm.state import StatesGroup, State

class AdminDrug(StatesGroup):
    name = State()
    uses = State()
    side = State()
    dosage = State()
    price_min = State()
    price_max = State()
    call_center = State()
    alternatives = State()

class AdminPharmacy(StatesGroup):
    title = State()
    address = State()
    lat = State()      # location bosqichi sifatida ishlatyapsiz
    lon = State()
    phone = State()

class AdminDelete(StatesGroup):
    drug_id = State()
    pharmacy_id = State()

# ---------- Broadcast (promo / message) ----------
class AdminPromo(StatesGroup):
    waiting_photo = State()
    waiting_text = State()
    confirm = State()

class AdminBroadcast(StatesGroup):
    waiting_photo = State()
    waiting_text = State()
    confirm = State()
