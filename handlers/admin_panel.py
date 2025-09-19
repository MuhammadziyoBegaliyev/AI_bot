from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import settings
from utils.lang import get_lang
from locales import LOCALES

from keyboards.admin_inline import (
    admin_root_inline, admin_drugs_inline, admin_pharm_inline, admin_loc_inline, admin_pager_inline
)
from states.admin_panel import (
    AdminDrugAdd, AdminDrugDelete,
    AdminPharmacyAdd, AdminPharmacyDelete,
    AdminLocationAdd, AdminLocationDelete,
)
from database import SessionLocal
from database.crud import (
    add_drug, list_drugs, delete_drug,
    add_pharmacy, list_pharmacies, delete_pharmacy,
    add_location, list_locations, delete_location,
)

router = Router()

def is_admin(user_id: int) -> bool:
    try:
        return user_id in settings.ADMIN_IDS
    except Exception:
        return False

# ===================== ENTRY =====================
@router.message(F.text.regexp(r"^/admin\b"))
async def admin_entry(message: Message):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"])
        return
    await message.answer("🛠 <b>Admin panel</b>", reply_markup=admin_root_inline(lang))

# ===================== ROOT TABS =====================
@router.callback_query(F.data == "admin:root")
async def admin_root(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    if not is_admin(cb.from_user.id):
        await cb.message.answer(LOCALES[lang]["admin_only"]); await cb.answer(); return
    await cb.message.edit_text("🛠 <b>Admin panel</b>", reply_markup=admin_root_inline(lang))
    await cb.answer()

@router.callback_query(F.data == "admin:drugs")
async def admin_tab_drugs(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    if not is_admin(cb.from_user.id):
        await cb.message.answer(LOCALES[lang]["admin_only"]); await cb.answer(); return
    await cb.message.edit_text("📦 <b>Drugs</b>", reply_markup=admin_drugs_inline(lang))
    await cb.answer()

@router.callback_query(F.data == "admin:pharmacies")
async def admin_tab_pharm(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    if not is_admin(cb.from_user.id):
        await cb.message.answer(LOCALES[lang]["admin_only"]); await cb.answer(); return
    await cb.message.edit_text("🏥 <b>Pharmacies</b>", reply_markup=admin_pharm_inline(lang))
    await cb.answer()

@router.callback_query(F.data == "admin:locations")
async def admin_tab_locations(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    if not is_admin(cb.from_user.id):
        await cb.message.answer(LOCALES[lang]["admin_only"]); await cb.answer(); return
    await cb.message.edit_text("📍 <b>Locations</b>", reply_markup=admin_loc_inline(lang))
    await cb.answer()

# ===================== DRUGS: ADD =====================
@router.callback_query(F.data == "drug:add")
async def drug_add_start(cb: CallbackQuery, state: FSMContext):
    if not is_admin(cb.from_user.id): await cb.answer("No"); return
    await state.set_state(AdminDrugAdd.waiting_name)
    await cb.message.answer("Dori nomi (name):")
    await cb.answer()

@router.message(AdminDrugAdd.waiting_name, F.text)
async def drug_add_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await state.set_state(AdminDrugAdd.waiting_uses)
    await msg.answer("Qo‘llanilishi (uses):")

@router.message(AdminDrugAdd.waiting_uses, F.text)
async def drug_add_uses(msg: Message, state: FSMContext):
    await state.update_data(uses=msg.text.strip())
    await state.set_state(AdminDrugAdd.waiting_side)
    await msg.answer("Yon ta'siri (side_effects):")

@router.message(AdminDrugAdd.waiting_side, F.text)
async def drug_add_side(msg: Message, state: FSMContext):
    await state.update_data(side_effects=msg.text.strip())
    await state.set_state(AdminDrugAdd.waiting_dosage)
    await msg.answer("Doza (dosage):")

@router.message(AdminDrugAdd.waiting_dosage, F.text)
async def drug_add_dosage(msg: Message, state: FSMContext):
    await state.update_data(dosage=msg.text.strip())
    await state.set_state(AdminDrugAdd.waiting_price_min)
    await msg.answer("Narx MIN (example: 10000 yoki 10.5):")

@router.message(AdminDrugAdd.waiting_price_min, F.text)
async def drug_add_pmin(msg: Message, state: FSMContext):
    txt = msg.text.strip().replace(",", ".")
    try:
        v = float(txt)
    except Exception:
        await msg.answer("❗️Noto‘g‘ri format. Raqam kiriting.")
        return
    await state.update_data(price_min=v)
    await state.set_state(AdminDrugAdd.waiting_price_max)
    await msg.answer("Narx MAX:")

@router.message(AdminDrugAdd.waiting_price_max, F.text)
async def drug_add_pmax(msg: Message, state: FSMContext):
    txt = msg.text.strip().replace(",", ".")
    try:
        v = float(txt)
    except Exception:
        await msg.answer("❗️Noto‘g‘ri format. Raqam kiriting.")
        return
    await state.update_data(price_max=v)
    await state.set_state(AdminDrugAdd.waiting_call_center)
    await msg.answer("Call-center (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminDrugAdd.waiting_call_center, F.text)
async def drug_add_cc(msg: Message, state: FSMContext):
    cc = None if msg.text.strip() == "-" else msg.text.strip()
    await state.update_data(call_center=cc)
    await state.set_state(AdminDrugAdd.waiting_alternatives)
    await msg.answer("Muqobillar (',' bilan, yo‘q bo‘lsa '-' yozing):")

@router.message(AdminDrugAdd.waiting_alternatives, F.text)
async def drug_add_save(msg: Message, state: FSMContext):
    data = await state.get_data()
    alt = None if msg.text.strip() == "-" else msg.text.strip()
    async with SessionLocal() as db:
        d = await add_drug(db, **data, alternatives=alt)
    await state.clear()
    await msg.answer(f"✅ Qo‘shildi: {d.name} (id={d.id})")

# ===================== DRUGS: LIST / DELETE =====================
PAGE_SIZE = 10

@router.callback_query(F.data == "drug:list")
async def drug_list(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    async with SessionLocal() as db:
        items = await list_drugs(db, limit=1000)
    text = "📃 <b>Dorilar</b>:\n"
    page = 1
    start = 0; end = min(len(items), PAGE_SIZE)
    if not items:
        text += "—"
    else:
        text += "\n".join([f"{d.id}) {d.name} [{d.price_min}-{d.price_max}]" for d in items[start:end]])
    has_next = len(items) > end
    await cb.message.answer(text, reply_markup=admin_pager_inline("drugs", page, has_next))
    await cb.answer()

@router.callback_query(F.data.startswith("pager:drugs:"))
async def drug_pager(cb: CallbackQuery):
    page = int(cb.data.split(":")[-1])
    async with SessionLocal() as db:
        items = await list_drugs(db, limit=1000)
    start = (page-1)*PAGE_SIZE; end = min(len(items), page*PAGE_SIZE)
    text = "📃 <b>Dorilar</b>:\n"
    if start >= len(items):
        text += "—"
        has_next = False
    else:
        text += "\n".join([f"{d.id}) {d.name} [{d.price_min}-{d.price_max}]" for d in items[start:end]])
        has_next = len(items) > end
    await cb.message.edit_text(text, reply_markup=admin_pager_inline("drugs", page, has_next))
    await cb.answer()

@router.callback_query(F.data == "drug:del")
async def drug_del_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminDrugDelete.waiting_id)
    await cb.message.answer("O‘chirish uchun dori ID kiriting:")
    await cb.answer()

@router.message(AdminDrugDelete.waiting_id, F.text.regexp(r"^\d+$"))
async def drug_do_del(msg: Message, state: FSMContext):
    async with SessionLocal() as db:
        await delete_drug(db, int(msg.text))
    await state.clear()
    await msg.answer("🗑 O‘chirildi.")

# ===================== PHARMACIES =====================
@router.callback_query(F.data == "ph:add")
async def ph_add_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminPharmacyAdd.waiting_title)
    await cb.message.answer("Apteka nomi:")
    await cb.answer()

@router.message(AdminPharmacyAdd.waiting_title, F.text)
async def ph_add_title(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text.strip())
    await state.set_state(AdminPharmacyAdd.waiting_lat)
    await msg.answer("Latitude (41.285 kabi):")

@router.message(AdminPharmacyAdd.waiting_lat, F.text)
async def ph_add_lat(msg: Message, state: FSMContext):
    try:
        lat = float(msg.text.strip().replace(",", "."))
    except Exception:
        await msg.answer("❗️Raqam kiriting."); return
    await state.update_data(lat=lat)
    await state.set_state(AdminPharmacyAdd.waiting_lon)
    await msg.answer("Longitude (69.203 kabi):")

@router.message(AdminPharmacyAdd.waiting_lon, F.text)
async def ph_add_lon(msg: Message, state: FSMContext):
    try:
        lon = float(msg.text.strip().replace(",", "."))
    except Exception:
        await msg.answer("❗️Raqam kiriting."); return
    await state.update_data(lon=lon)
    await state.set_state(AdminPharmacyAdd.waiting_address)
    await msg.answer("Manzil:")

@router.message(AdminPharmacyAdd.waiting_address, F.text)
async def ph_add_addr(msg: Message, state: FSMContext):
    await state.update_data(address=msg.text.strip())
    await state.set_state(AdminPharmacyAdd.waiting_link)
    await msg.answer("Xarita havolasi (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminPharmacyAdd.waiting_link, F.text)
async def ph_add_save(msg: Message, state: FSMContext):
    data = await state.get_data()
    link = None if msg.text.strip() == "-" else msg.text.strip()
    kwargs = {**data, "link": link}
    async with SessionLocal() as db:
        p = await add_pharmacy(db, **kwargs)
    await state.clear()
    await msg.answer(f"✅ Apteka qo‘shildi: {p.title} (id={p.id})")

@router.callback_query(F.data == "ph:list")
async def ph_list(cb: CallbackQuery):
    async with SessionLocal() as db:
        items = await list_pharmacies(db, limit=1000)
    page = 1; start = 0; end = min(len(items), PAGE_SIZE)
    text = "📃 <b>Aptekalar</b>:\n"
    text += "—" if not items else "\n".join([f"{p.id}) {p.title} ({p.lat},{p.lon})" for p in items[start:end]])
    has_next = len(items) > end
    await cb.message.answer(text, reply_markup=admin_pager_inline("ph", page, has_next))
    await cb.answer()

@router.callback_query(F.data.startswith("pager:ph:"))
async def ph_pager(cb: CallbackQuery):
    page = int(cb.data.split(":")[-1])
    async with SessionLocal() as db:
        items = await list_pharmacies(db, limit=1000)
    start = (page-1)*PAGE_SIZE; end = min(len(items), page*PAGE_SIZE)
    text = "📃 <b>Aptekalar</b>:\n"
    text += "—" if start >= len(items) else "\n".join([f"{p.id}) {p.title} ({p.lat},{p.lon})" for p in items[start:end]])
    has_next = len(items) > end
    await cb.message.edit_text(text, reply_markup=admin_pager_inline("ph", page, has_next))
    await cb.answer()

@router.callback_query(F.data == "ph:del")
async def ph_del_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminPharmacyDelete.waiting_id)
    await cb.message.answer("O‘chirish uchun apteka ID kiriting:")
    await cb.answer()

@router.message(AdminPharmacyDelete.waiting_id, F.text.regexp(r"^\d+$"))
async def ph_do_del(msg: Message, state: FSMContext):
    async with SessionLocal() as db:
        await delete_pharmacy(db, int(msg.text))
    await state.clear()
    await msg.answer("🗑 O‘chirildi.")

# ===================== LOCATIONS (4 ta asosiy) =====================
@router.callback_query(F.data == "loc:add")
async def loc_add_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminLocationAdd.waiting_title)
    await cb.message.answer("Filial nomi (Locations bo‘limi uchun):")
    await cb.answer()

@router.message(AdminLocationAdd.waiting_title, F.text)
async def loc_add_title(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text.strip())
    await state.set_state(AdminLocationAdd.waiting_address)
    await msg.answer("Manzil:")

@router.message(AdminLocationAdd.waiting_address, F.text)
async def loc_add_addr(msg: Message, state: FSMContext):
    await state.update_data(address=msg.text.strip())
    await state.set_state(AdminLocationAdd.waiting_link)
    await msg.answer("Xarita havolasi (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminLocationAdd.waiting_link, F.text)
async def loc_add_link(msg: Message, state: FSMContext):
    link = None if msg.text.strip() == "-" else msg.text.strip()
    await state.update_data(link=link)
    await state.set_state(AdminLocationAdd.waiting_point)
    await msg.answer("📍 Endi lokatsiya yuboring (chat joyidan «Send location»):")

@router.message(AdminLocationAdd.waiting_point, F.location)
async def loc_add_point(msg: Message, state: FSMContext):
    data = await state.get_data()
    lat = msg.location.latitude
    lon = msg.location.longitude
    async with SessionLocal() as db:
        loc = await add_location(db,
                                 title=data["title"], address=data["address"],
                                 link=data.get("link"), lat=lat, lon=lon)
    await state.clear()
    await msg.answer(f"✅ Location qo‘shildi: {loc.title} (id={loc.id})")

@router.callback_query(F.data == "loc:list")
async def loc_list(cb: CallbackQuery):
    async with SessionLocal() as db:
        items = await list_locations(db, limit=1000)
    page = 1; start = 0; end = min(len(items), PAGE_SIZE)
    text = "📃 <b>Locations</b>:\n"
    text += "—" if not items else "\n".join([f"{l.id}) {l.title} ({l.lat},{l.lon})" for l in items[start:end]])
    has_next = len(items) > end
    await cb.message.answer(text, reply_markup=admin_pager_inline("loc", page, has_next))
    await cb.answer()

@router.callback_query(F.data.startswith("pager:loc:"))
async def loc_pager(cb: CallbackQuery):
    page = int(cb.data.split(":")[-1])
    async with SessionLocal() as db:
        items = await list_locations(db, limit=1000)
    start = (page-1)*PAGE_SIZE; end = min(len(items), page*PAGE_SIZE)
    text = "📃 <b>Locations</b>:\n"
    text += "—" if start >= len(items) else "\n".join([f"{l.id}) {l.title} ({l.lat},{l.lon})" for l in items[start:end]])
    has_next = len(items) > end
    await cb.message.edit_text(text, reply_markup=admin_pager_inline("loc", page, has_next))
    await cb.answer()

@router.callback_query(F.data == "loc:del")
async def loc_del_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminLocationDelete.waiting_id)
    await cb.message.answer("O‘chirish uchun location ID kiriting:")
    await cb.answer()

@router.message(AdminLocationDelete.waiting_id, F.text.regexp(r"^\d+$"))
async def loc_do_del(msg: Message, state: FSMContext):
    async with SessionLocal() as db:
        await delete_location(db, int(msg.text))
    await state.clear()
    await msg.answer("🗑 O‘chirildi.")
