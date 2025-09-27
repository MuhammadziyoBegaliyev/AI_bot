from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

import io
import pandas as pd  # requirements.txt ga: pandas, xlsxwriter qo'shing

from filters.admin import AdminFilter
from locales import LOCALES
from utils.lang import get_lang

from keyboards.reply import location_request_kb
from keyboards.admin_inline import (
    admin_root_inline, admin_drugs_inline, admin_pharm_inline,
    admin_loc_inline, admin_main_kb, bc_yes_no_photo_kb, bc_preview_kb
)


from states.admin import (
    AdminDrug, AdminPharmacy, AdminDelete,
    AdminPromo, AdminBroadcast
)

from database import SessionLocal
from database.crud import (
    top_searches, list_feedbacks,
    add_drug, list_drugs, delete_drug,
    add_pharmacy, list_pharmacies, delete_pharmacy,
    list_all_users,          # siz CRUDga qo'shgansiz (tg_id, full_name, age, phone, lang, ...)
    list_searches            # foydalanuvchi qidiruvlari (user_id, query, created_at)
)

router = Router()

# -------------------------------
# Admin panelga kirish
# -------------------------------
@router.message(AdminFilter(), Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer("🛠 Admin panel", reply_markup=admin_root_inline(lang))

# -------------------------------
# Statistikalar / ro‘yxatlar
# -------------------------------
@router.callback_query(AdminFilter(), F.data == "adm:top")
async def cb_top(cb: CallbackQuery):
    async with SessionLocal() as db:
        rows = await top_searches(db)
    text = "📈 Top qidiruvlar:\n" + (
        "\n".join([f"{i+1}) {t} — {c}" for i, (t, c) in enumerate(rows)]) if rows else "—"
    )
    await cb.message.answer(text)
    await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:fb")
async def cb_fb(cb: CallbackQuery):
    async with SessionLocal() as db:
        fbs = await list_feedbacks(db)
    txt = "💬 Feedbacklar:\n" + (
        "\n".join([
            f"id={f.id} rating={f.rating or '-'} photo={bool(f.complaint_photo_id)} "
            f"loc={f.complaint_location or '-'}"
            for f in fbs
        ]) if fbs else "—"
    )
    await cb.message.answer(txt)
    await cb.answer()

# -------------------------------
# Dori CRUD
# -------------------------------
@router.callback_query(AdminFilter(), F.data == "adm:drug_add")
async def cb_drug_add(cb: CallbackQuery, state: FSMContext):
    await adb_add(cb.message, state); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:drug_list")
async def cb_drug_list(cb: CallbackQuery):
    await adb_list(cb.message); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:drug_del")
async def cb_drug_del(cb: CallbackQuery, state: FSMContext):
    await adb_del(cb.message, state); await cb.answer()

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
    txt = "📃 Dorilar:\n" + (
        "\n".join([f"{d.id}) {d.name} [{d.price_min}-{d.price_max}]" for d in items]) if items else "—"
    )
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
# Apteka CRUD — location orqali
# -------------------------------
@router.callback_query(AdminFilter(), F.data == "adm:ph_add")
async def cb_ph_add(cb: CallbackQuery, state: FSMContext):
    await aph_add(cb.message, state); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:ph_list")
async def cb_ph_list(cb: CallbackQuery):
    await aph_list(cb.message); await cb.answer()

@router.callback_query(AdminFilter(), F.data == "adm:ph_del")
async def cb_ph_del(cb: CallbackQuery, state: FSMContext):
    await aph_del(cb.message, state); await cb.answer()

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
    await state.set_state(AdminPharmacy.lat)
    await message.answer("📍 Endi lokatsiyani yuboring:", reply_markup=location_request_kb("uz"))

@router.message(AdminPharmacy.lat, F.location)
async def aph_location(message: Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await state.set_state(AdminPharmacy.phone)
    await message.answer("Telefon (yo‘q bo‘lsa '-' yozing):")

@router.message(AdminPharmacy.lat, F.text)
async def aph_latlon_fallback(message: Message, state: FSMContext):
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
    txt = "📃 Aptekalar:\n" + (
        "\n".join([f"{p.id}) {p.title} ({p.lat},{p.lon}) — {p.address}" for p in items]) if items else "—"
    )
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

# -------------------------------
# 📢 Aksiya va ✉️ Habar — Broadcast oqimi
# -------------------------------
@router.callback_query(AdminFilter(), F.data.in_({"adm:promo", "adm:msg"}))
async def bc_entry(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    bc_type = "promo" if cb.data == "adm:promo" else "msg"
    await state.update_data(bc_type=bc_type, photo_id=None, text=None)
    await state.set_state(AdminPromo.waiting_photo if bc_type == "promo" else AdminBroadcast.waiting_photo)
    t = LOCALES.get(lang, LOCALES["uz"])
    ask = t.get("adm_bc_ask_photo", "📷 Rasm qo‘shasizmi?")
    await cb.message.answer(ask, reply_markup=bc_yes_no_photo_kb(lang))
    await cb.answer()

@router.callback_query(AdminFilter(), F.data.startswith("bc:want:"))
async def bc_want_photo(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    want = cb.data.split(":")[-1]  # yes | no
    data = await state.get_data()
    bc_type = data.get("bc_type", "promo")
    if want == "yes":
        await (state.set_state(AdminPromo.waiting_photo) if bc_type == "promo"
               else state.set_state(AdminBroadcast.waiting_photo))
        await cb.message.answer(LOCALES.get(lang, LOCALES["uz"]).get("adm_bc_send_photo", "Rasm yuboring."))
    else:
        await (state.set_state(AdminPromo.waiting_text) if bc_type == "promo"
               else state.set_state(AdminBroadcast.waiting_text))
        await cb.message.answer(LOCALES.get(lang, LOCALES["uz"]).get("adm_bc_send_text", "Matnni yuboring."))
    await cb.answer()

@router.message(AdminPromo.waiting_photo, F.photo)
@router.message(AdminBroadcast.waiting_photo, F.photo)
async def bc_got_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo_id=file_id)
    data = await state.get_data()
    bc_type = data.get("bc_type", "promo")
    await (state.set_state(AdminPromo.waiting_text) if bc_type == "promo"
           else state.set_state(AdminBroadcast.waiting_text))
    await message.answer("✅ Rasm qabul qilindi. Endi matnni yuboring.")

@router.message(AdminPromo.waiting_text, F.text)
@router.message(AdminBroadcast.waiting_text, F.text)
async def bc_got_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(text=message.text.strip())
    data = await state.get_data()
    photo_id = data.get("photo_id")
    txt = data.get("text")
    await (state.set_state(AdminPromo.confirm) if data.get("bc_type") == "promo"
           else state.set_state(AdminBroadcast.confirm))

    if photo_id:
        await message.answer_photo(photo_id, caption=txt, reply_markup=bc_preview_kb(lang))
    else:
        await message.answer(txt, reply_markup=bc_preview_kb(lang))

@router.callback_query(AdminFilter(), F.data == "bc:edit:text")
async def bc_edit_text(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await (state.set_state(AdminPromo.waiting_text) if data.get("bc_type") == "promo"
           else state.set_state(AdminBroadcast.waiting_text))
    await cb.message.answer("✏️ Yangi matnni yuboring.")
    await cb.answer()

@router.callback_query(AdminFilter(), F.data == "bc:edit:photo")
async def bc_edit_photo(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await (state.set_state(AdminPromo.waiting_photo) if data.get("bc_type") == "promo"
           else state.set_state(AdminBroadcast.waiting_photo))
    await cb.message.answer("🖼 Yangi rasmni yuboring.")
    await cb.answer()

@router.callback_query(AdminFilter(), F.data == "bc:cancel")
async def bc_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("❌ Bekor qilindi.")
    await cb.answer()

@router.callback_query(AdminFilter(), F.data == "bc:send")
async def bc_send(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    data = await state.get_data()
    txt = data.get("text", "")
    photo_id = data.get("photo_id")
    count_ok = 0

    async with SessionLocal() as db:
        try:
            users = await list_all_users(db)  # model yoki tuple bo‘lishi mumkin
        except Exception:
            users = []

    bot = cb.message.bot
    for row in users:
        tg_id = (
            row[0] if isinstance(row, (list, tuple)) else
            getattr(row, "tg_id", None) or getattr(row, "telegram_id", None) or getattr(row, "id", None)
        )
        if not tg_id:
            continue
        try:
            if photo_id:
                await bot.send_photo(tg_id, photo_id, caption=txt)
            else:
                await bot.send_message(tg_id, txt)
            count_ok += 1
        except Exception:
            pass

    await state.clear()
    done = LOCALES.get(lang, LOCALES["uz"]).get("adm_bc_done", "✅ Yuborildi")
    await cb.message.answer(f"{done}: {count_ok} ta foydalanuvchiga.")
    await cb.answer()

# -------------------------------
# 📊 Foydalanuvchilar ma’lumoti — Excel eksport
# -------------------------------
@router.callback_query(AdminFilter(), F.data == "admin:users_export")
async def cb_users_export(cb: CallbackQuery):
    # foydalanuvchilar, fikrlar va qidiruvlarni bitta .xlsx faylga
    async with SessionLocal() as db:
        users = await list_all_users(db)
        fbs   = await list_feedbacks(db)
        srchs = await list_searches(db)

    # Users
    df_users = pd.DataFrame([{
        "UserID": getattr(u, "tg_id", None) or getattr(u, "telegram_id", None) or getattr(u, "id", None),
        "Ism Familiya": getattr(u, "full_name", None),
        "Yosh": getattr(u, "age", None),
        "Telefon": getattr(u, "phone", None),
        "Til": getattr(u, "lang", None),
        "Username": f"@{getattr(u, 'username', '')}" if getattr(u, "username", None) else "",
        "Ro‘yxatga olingan": getattr(u, "created_at", None),
    } for u in users])

    # Feedbacks
    df_fb = pd.DataFrame([{
        "UserID": getattr(f, "user_id", None),
        "Matn": getattr(f, "text", None),
        "Baho": getattr(f, "rating", None),
        "Shikoyat foto": bool(getattr(f, "complaint_photo_id", None)),
        "Shikoyat lokatsiya": getattr(f, "complaint_location", None),
        "Sana": getattr(f, "created_at", None),
    } for f in fbs])

    # Searches
    df_search = pd.DataFrame([{
        "UserID": getattr(s, "user_id", None),
        "So‘rov": getattr(s, "query", None),
        "Sana": getattr(s, "created_at", None),
    } for s in srchs])

    # Excel fayl
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df_users.to_excel(writer, index=False, sheet_name="Users")
        df_fb.to_excel(writer, index=False, sheet_name="Feedbacks")
        df_search.to_excel(writer, index=False, sheet_name="Searches")
    out.seek(0)

    await cb.message.answer_document(
        document=BufferedInputFile(out.read(), filename="users_report.xlsx"),
        caption="📊 Foydalanuvchilar hisobot fayli"
    )
    await cb.answer()
