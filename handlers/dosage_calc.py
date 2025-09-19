# path: handlers/dosage_calc.py
from aiogram import Router
router = Router()
# Intentionally left blank. 'dose:' callback handled in handlers/search.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from locales import LOCALES
from utils.dosage import suggest_dose
from utils.lang import get_lang, require_user_and_lang

router = Router()

@router.callback_query(F.data.startswith("dose:"))
async def dose_calc(cb: CallbackQuery):
    lang = (cb.from_user.language_code or "uz")[:2]
    # Demo: foydalanuvchi yoshi DB-dan olinmadi — keyinchalik qo‘shing
    age = 25
    text = suggest_dose("paracetamol", age)
    await cb.message.answer(f"{LOCALES[lang]['dose_calc']}:\n{text}")
    await cb.answer()
