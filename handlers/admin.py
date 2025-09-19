# path: handlers/admin.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.admin import AdminFilter
from locales import LOCALES
from utils.lang import get_lang
from keyboards.reply import location_request_kb  # sizda bor (foydalanuvchi joyini yuborish uchun)

from states.admin import AdminDrug, AdminPharmacy, AdminDelete
from database import SessionLocal
from database.crud import (
    top_searches, list_feedbacks,
    add_drug, list_drugs, delete_drug,
    add_pharmacy, list_pharmacies, delete_pharmacy,
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# -------------------------------
# Inline admin keyboard
# -------------------------------
def admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📈 Top qidiruvlar", callback_data="adm:top"),
            InlineKeyboardButton(text="💬 Feedbacklar", callback_data="adm:fb"),
        ],
        [
            InlineKeyboardButton(text="➕ Dori qo‘shish", callback_data="adm:drug_add"),
            InlineKeyboardButton(text="📃 Dorilar", callback_data="adm:drug_list"),
            InlineKeyboardButton(text="🗑 Dori o‘chirish", callback_data="adm:drug_del"),
        ],
        [
            InlineKeyboardButton(text="➕ Apteka qo‘shish", callback_data="adm:ph_add"),
            InlineKeyboardButton(text="📃 Aptekalar", callback_data="adm:ph_list"),
            InlineKeyboardButton(text="🗑 Apteka o‘chirish", callback_data="adm:ph_del"),
        ],
    ])

# -------------------------------
# Admin panelga kirish
# -------------------------------
@router.message(AdminFilter(), F.text.regexp(r"^/admin\b"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["admin"], reply_markup=admin_menu_kb())

# --- Inline callback’lar menyuni boshqaradi ---
@router.callback_query(AdminFilter(), F.data == "adm:top")
async def cb_top(cb: CallbackQuery):
    async with SessionLocal() as db:
        rows = await top_searches(db)
    text = "📈 Top:\n" + ("\n".join([f"{i+1}) {t} — {c}" for i, (t, c) in enumerate(rows)]) if rows else "—")
    await cb.message.answer(text)
    await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:fb")
async def cb_fb(cb: CallbackQuery):
    async with SessionLocal() as db:
        fbs = await list_feedbacks(db)
    txt = "💬 Feedbacks:\n" + (
        "\n".join([
            f"id={f.id} rating={f.rating or '-'} photo={bool(f.complaint_photo_id)} loc={f.complaint_location or '-'}"
            for f in fbs
        ]) if fbs else "—"
    )
    await cb.message.answer(txt); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:drug_add")
async def cb_drug_add(cb: CallbackQuery, state: FSMContext):
    await adb_add(cb.message, state); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:drug_list")
async def cb_drug_list(cb: CallbackQuery):
    await adb_list(cb.message); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:drug_del")
async def cb_drug_del(cb: CallbackQuery, state: FSMContext):
    await adb_del(cb.message, state); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:ph_add")
async def cb_ph_add(cb: CallbackQuery, state: FSMContext):
    await aph_add(cb.message, state); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:ph_list")
async def cb_ph_list(cb: CallbackQuery):
    await aph_list(cb.message); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:ph_del")
async def cb_ph_del(cb: CallbackQuery, state: FSMContext):
    await aph_del(cb.message, state); await cb.answer()

# -------------------------------
# Dori CRUD (o‘zgarmagan, faqat foydali validatsiyalar bor)
# -------------------------------
@router.message(AdminFilter(), F.text == "/adb_add")
async def adb_add(message: Message, state: FSMContext):
    await state.set_state(AdminDrug.name)
    await message.answer("Dori nomi:")

@router.message(AdminDrug.name, F.text)
async def adb_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AdminDrug.uses)
    await message.answer("Qo‘llanilishi:")

@router.message(AdminDrug.uses, F.text)
async def adb_uses(message: Message, state: FSMContext):
    await state.update_data(uses=message.text.strip())
    await state.set_state(AdminDrug.side)
    await message.answer("Yon ta'siri:")

@router.message(AdminDrug.side, F.text)
async def adb_side(message: Message, state: FSMContext):
    await state.update_data(side_effects=message.text.strip())
    await state.set_state(AdminDrug.dosage)
    await message.answer("Doza:")

@router.message(AdminDrug.dosage, F.text)
async def adb_dosage(message: Message, state: FSMContext):
    await state.update_data(dosage=message.text.strip())
    await state.set_state(AdminDrug.price_min)
    await message.answer("Narx min (10000 yoki 10.5):")

@router.message(AdminDrug.price_min, F.text)
async def adb_pmin(message: Message, state: FSMContext):
    txt = message.text.strip().replace(",", ".")
    try:
        v = float(txt)
    except Exception:
        await message.answer("❗️ Noto‘g‘ri format. Raqam kiriting.")
        return
    await state.update_data(price_min=v)
    await state.set_state(AdminDrug.price_max)
    await message.answer("Narx max:")

@router.message(AdminDrug.price_max, F.text)
async def adb_pmax(message: Message, state: FSMContext):
    txt = message.text.strip().replace(",", ".")
    try:
        v = float(txt)
    except Exception:
        await message.answer("❗️ Noto‘g‘ri format. Raqam kiriting.")
        return
    await state.update_data(price_max=v)
    await state.set_state(AdminDrug.call_center)
    await message.answer("Call-center (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminDrug.call_center, F.text)
async def adb_cc(message: Message, state: FSMContext):
    cc = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(call_center=cc)
    await state.set_state(AdminDrug.alternatives)
    await message.answer("Muqobillar (',' bilan, yo‘q bo‘lsa '-' yozing):")

@router.message(AdminDrug.alternatives, F.text)
async def adb_alt(message: Message, state: FSMContext):
    data = await state.get_data()
    alt = None if message.text.strip() == "-" else message.text.strip()

    if "title" in data and "name" not in data:
        data["name"] = data.pop("title")

    async with SessionLocal() as db:
        d = await add_drug(db, **data, alternatives=alt)

    await state.clear()
    await message.answer(f"✅ Qo‘shildi: {d.name} (id={d.id})")

@router.message(AdminFilter(), F.text == "/adb_list")
async def adb_list(message: Message):
    async with SessionLocal() as db:
        items = await list_drugs(db)
    txt = "📃 Dorilar:\n" + ("\n".join([f"{d.id}) {d.name} [{d.price_min}-{d.price_max}]" for d in items]) if items else "—")
    await message.answer(txt)

@router.message(AdminFilter(), F.text == "/adb_del")
async def adb_del(message: Message, state: FSMContext):
    await state.set_state(AdminDelete.drug_id)
    await message.answer("O‘chirish uchun dori ID:")

@router.message(AdminDelete.drug_id, F.text.regexp(r"^\d+$"))
async def adb_do_del(message: Message, state: FSMContext):
    async with SessionLocal() as db:
        await delete_drug(db, int(message.text))
    await state.clear()
    await message.answer("🗑 O‘chirildi.")

# -------------------------------
# Apteka CRUD — lokatsiyani location orqali olish!
# -------------------------------
@router.message(AdminFilter(), F.text == "/aph_add")
async def aph_add(message: Message, state: FSMContext):
    await state.set_state(AdminPharmacy.title)
    await message.answer("Apteka nomi (filial nomi):")

@router.message(AdminPharmacy.title, F.text)
async def aph_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AdminPharmacy.address)
    await message.answer("Manzil (yozib bering):")

@router.message(AdminPharmacy.address, F.text)
async def aph_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    # Location so‘raymiz
    await state.set_state(AdminPharmacy.lat)  # lat holatidan foydalanamiz
    await message.answer("📍 Endi lokatsiyani yuboring:", reply_markup=location_request_kb("uz"))

# AdminPharmacy.lat holatida ikkita handler: F.location va F.text (fallback)
@router.message(AdminPharmacy.lat, F.location)
async def aph_location(message: Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await state.set_state(AdminPharmacy.phone)
    await message.answer("Telefon (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminPharmacy.lat, F.text)
async def aph_latlon_fallback(message: Message, state: FSMContext):
    # Agar baribir matn yuborsa — lat/lon ni vergul bilan kiritsin
    txt = message.text.strip().replace(" ", "")
    if "," in txt:
        la, lo = txt.split(",", 1)
        try:
            la = float(la.replace(",", "."))
            lo = float(lo.replace(",", "."))
        except Exception:
            await message.answer("❗️ Noto‘g‘ri format. '41.123,69.123' tarzida yuboring yoki lokatsiya jo‘nating.")
            return
        await state.update_data(lat=la, lon=lo)
        await state.set_state(AdminPharmacy.phone)
        await message.answer("Telefon (yo‘q bo‘lsa '-' yozing):")
    else:
        await message.answer("❗️ Lokatsiya jo‘nating yoki '41.123,69.123' ko‘rinishida kiriting.")

@router.message(AdminPharmacy.phone, F.text)
async def aph_save(message: Message, state: FSMContext):
    phone = None if message.text.strip() == "-" else message.text.strip()
    data = await state.get_data()

    # faqat model ustunlari:
    kwargs = {
        "title":   data["title"],
        "address": data["address"],
        "lat":     data["lat"],
        "lon":     data["lon"],
    }
    if phone:
        kwargs["phone"] = phone

    async with SessionLocal() as db:
        p = await add_pharmacy(db, **kwargs)

    await state.clear()
    await message.answer(f"✅ Apteka qo‘shildi: {p.title} (id={p.id})")

@router.message(AdminFilter(), F.text == "/aph_list")
async def aph_list(message: Message):
    async with SessionLocal() as db:
        items = await list_pharmacies(db)
    txt = "📃 Aptekalar:\n" + ("\n".join([f"{p.id}) {p.title} ({p.lat},{p.lon}) — {p.address}" for p in items]) if items else "—")
    await message.answer(txt)

@router.message(AdminFilter(), F.text == "/aph_del")
async def aph_del(message: Message, state: FSMContext):
    await state.set_state(AdminDelete.pharmacy_id)
    await message.answer("O‘chirish uchun apteka ID:")

@router.message(AdminDelete.pharmacy_id, F.text.regexp(r"^\d+$"))
async def aph_do_del(message: Message, state: FSMContext):
    async with SessionLocal() as db:
        await delete_pharmacy(db, int(message.text))
    await state.clear()
    await message.answer("🗑 O‘chirildi.")
