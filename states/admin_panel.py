from aiogram.fsm.state import StatesGroup, State

# DRUG
class AdminDrugAdd(StatesGroup):
    waiting_name = State()
    waiting_uses = State()
    waiting_side = State()
    waiting_dosage = State()
    waiting_price_min = State()
    waiting_price_max = State()
    waiting_call_center = State()
    waiting_alternatives = State()

class AdminDrugDelete(StatesGroup):
    waiting_id = State()

# PHARMACY
class AdminPharmacyAdd(StatesGroup):
    waiting_title = State()
    waiting_lat = State()
    waiting_lon = State()
    waiting_address = State()
    waiting_link = State()

class AdminPharmacyDelete(StatesGroup):
    waiting_id = State()

# LOCATION (foydalanuvchi bo‘limidagi to‘rtlik)
class AdminLocationAdd(StatesGroup):
    waiting_title = State()
    waiting_address = State()
    waiting_link = State()
    waiting_point = State()

class AdminLocationDelete(StatesGroup):
    waiting_id = State()
