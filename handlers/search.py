# path: handlers/search.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from filters.registered import RegisteredFilter
from locales import LOCALES

from states.search import SearchFlow
from states.feedback import FeedbackFlow

from database import SessionLocal
from database.crud import find_drug_by_name, log_search, all_pharmacies

from keyboards.inline import drug_actions, back_kb
from keyboards.reply import main_menu

from utils.geo import nearest
from utils.ocr_stub import detect_name_from_photo
from utils.lang import get_lang
from utils.dosage import suggest_dose

router = Router()

# =========================================================
# 0) Intercept: qidiruv holatida "Fikr bildirish" bosilsa
#    (umumiy text handleridan YUQORIDA turishi kerak!)
# =========================================================
@router.message(
    RegisteredFilter(),
    SearchFlow.waiting_query,
    F.text.func(lambda s: s and s.replace("💬", "").strip().lower() in {"fikr bildirish", "feedback", "отзыв"}),
    F.text.func(lambda s: s and not s.startswith("/"))
)
async def goto_feedback_from_search(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(FeedbackFlow.waiting_text)
    await message.answer(LOCALES[lang]["feedback_ask"], reply_markup=back_kb(lang, "menu"))

# =========================================
# 1) Qidiruvga kirish
# =========================================
@router.message(RegisteredFilter(), F.text.in_({"🔎 Qidiruv", "🔎 Search", "🔎 Поиск"}))
async def enter_search(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(SearchFlow.waiting_query)
    await message.answer(LOCALES[lang]["search_ask"])

# =========================================
# 2) Nomi bo'yicha qidiruv
# =========================================
@router.message(RegisteredFilter(), SearchFlow.waiting_query, F.text)
async def search_by_name(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    q = message.text.strip()

    async with SessionLocal() as db:
        rows = await find_drug_by_name(db, q)
        if not rows:
            await message.answer(LOCALES[lang]["search_none"], reply_markup=back_kb(lang, "menu"))
            return
        d = rows[0]
        await log_search(db, user_id=message.from_user.id, term=q)

    alt = f"\n<b>{LOCALES[lang]['alternatives']}:</b> {d.alternatives}" if d.alternatives else ""
    text = (
        f"<b>{LOCALES[lang]['drug_info']}</b>\n"
        f"<b>Nom:</b> {d.name}\n"
        f"<b>{LOCALES[lang]['uses']}:</b> {d.uses}\n"
        f"<b>{LOCALES[lang]['side']}:</b> {d.side_effects}\n"
        f"<b>{LOCALES[lang]['dose']}:</b> {d.dosage}\n"
        f"<b>{LOCALES[lang]['price']}:</b> {d.price_min} — {d.price_max}\n"
        f"<b>{LOCALES[lang]['call']}:</b> {d.call_center or '-'}"
        f"{alt}\n\n{LOCALES[lang]['send_location']}"
    )
    await message.answer(text, reply_markup=drug_actions(lang, d.id))

# =========================================
# 3) Rasm orqali qidiruv (stub OCR)
# =========================================
@router.message(RegisteredFilter(), SearchFlow.waiting_query, F.photo)
async def search_by_photo(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    name = detect_name_from_photo()
    if not name:
        await message.answer(LOCALES[lang]["search_none"], reply_markup=back_kb(lang, "menu"))
        return
    fake = message.model_copy(update={"text": name})
    await search_by_name(fake, state)

# =========================================
# 4) Eng yaqin apteka (lokatsiya)
#    — faqat FSM holati yo‘q bo‘lsa ishlaydi (default_state)
# =========================================
@router.message(RegisteredFilter(), default_state, F.location)
async def nearest_pharmacy(message: Message):
    lang = await get_lang(message.from_user.id)
    async with SessionLocal() as db:
        phs = await all_pharmacies(db)

    if not phs:
        await message.answer("No pharmacies in DB yet.")
        return

    items = [(p.id, p.title, p.lat, p.lon) for p in phs]
    (pid, title, _, _), dist = nearest(
        message.location.latitude, message.location.longitude, items
    )
    await message.answer(f"{LOCALES[lang]['nearest']}: {title} (~{dist:.2f} km)")

# =========================================
# 5) Doza kalkulyatori (demo)
# =========================================
@router.callback_query(F.data.startswith("dose:"))
async def dose_cb(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    dose_text = suggest_dose("paracetamol", age=25)
    await cb.message.answer(f"{LOCALES[lang]['dose_calc']}:\n{dose_text}")
    await cb.answer()

# =========================================
# 6) Orqaga tugmalari
# =========================================
@router.callback_query(F.data.startswith("back:"))
async def back_cb(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    target = cb.data.split(":", 1)[1]

    # State'ni tozalab yuboramiz — foydalanuvchi to‘liq qaytsin
    await state.clear()

    if target == "menu":
        await cb.message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))
    elif target == "search":
        await cb.message.answer(LOCALES[lang]["search_ask"])
    await cb.answer()

# =========================================
# 7) ➕ Yana qidirish
# =========================================
@router.callback_query(F.data == "more_search")
async def more_search(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(SearchFlow.waiting_query)
    await cb.message.answer(LOCALES[lang]["search_ask"])
    await cb.answer()
