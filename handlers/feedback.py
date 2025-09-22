# path: handlers/feedback.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.registered import RegisteredFilter
from locales import LOCALES
from utils.lang import get_lang

from states.feedback import FeedbackFlow
from database import SessionLocal
from database.crud import create_feedback, set_feedback_rating
from database.crud import get_user_by_tg  # foydalanuvchi ma'lumoti uchun

from keyboards.inline import fb_type_kb, fb_stars_kb, complaint_actions_kb
from keyboards.reply import main_menu
from config import settings

router = Router()

# ====== KIRISH: "💬 Fikr bildirish" (main menu dan) ======
@router.message(RegisteredFilter(), F.text.in_({"💬 Fikr bildirish", "💬 Feedback", "💬 Отзыв"}))
async def fb_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(FeedbackFlow.choosing_type)
    await message.answer(LOCALES[lang]["fb_choose"], reply_markup=fb_type_kb(lang))

# ====== TUR TANLASH: Fikr / Shikoyat ======
@router.callback_query(F.data.startswith("fb:type:"))
async def fb_choose_type(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    _, _, ftype = cb.data.split(":")
    if ftype == "review":
        # baho -> matn
        await state.set_state(FeedbackFlow.rating_wait)
        await cb.message.edit_text(LOCALES[lang]["fb_rate_ask"], reply_markup=fb_stars_kb(lang))
    else:
        # shikoyat matni
        await state.set_state(FeedbackFlow.complaint_text)
        await cb.message.edit_text(LOCALES[lang]["cmp_ask_text"], reply_markup=complaint_actions_kb(lang))
    await cb.answer()

# ====== BAHO TANLASH (1..5) ======
@router.callback_query(F.data.startswith("fb:rate:"))
async def fb_rate(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    rating = int(cb.data.split(":")[2])
    await state.update_data(rating=rating)
    await state.set_state(FeedbackFlow.review_text)
    await cb.message.edit_text(LOCALES[lang]["fb_text_ask"])
    await cb.answer()

# ====== FIKR MATNI QABULI ======
@router.message(FeedbackFlow.review_text, F.text)
async def fb_got_review(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    data = await state.get_data()
    rating = int(data.get("rating", 0) or 0)
    text = message.text.strip()

    # DB ga yozish
    async with SessionLocal() as db:
        fb = await create_feedback(db, user_id=message.from_user.id, text=text)
        if rating:
            await set_feedback_rating(db, fb.id, rating)

        # foydalanuvchi profilini oldik
        u = await get_user_by_tg(db, message.from_user.id)

    # Guruhga yuborish
    await _send_to_group_review(message, lang, rating, text, u)

    await state.clear()
    await message.answer(t["fb_thanks"], reply_markup=main_menu(lang))

# ====== SHIKOYAT MATNI QABULI ======
@router.message(FeedbackFlow.complaint_text, F.text)
async def cmp_got_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(text=message.text.strip(), photo_id=None, loc=None)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(LOCALES[lang]["cmp_more"], reply_markup=complaint_actions_kb(lang))

# ====== SHIKOYAT: "Rasm yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:cphoto")
async def cmp_want_photo(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(FeedbackFlow.waiting_photo)
    await cb.message.answer(LOCALES[lang]["cmp_send_photo"])
    await cb.answer()

# ====== SHIKOYAT: Foydalanuvchi rasm yuboradi ======
@router.message(FeedbackFlow.waiting_photo, F.photo)
async def cmp_got_photo(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    file_id = message.photo[-1].file_id
    await state.update_data(photo_id=file_id)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(LOCALES[lang]["cmp_photo_ok"], reply_markup=complaint_actions_kb(lang))

# ====== SHIKOYAT: "Lokatsiyani yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:cloc")
async def cmp_want_loc(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(FeedbackFlow.waiting_location)
    await cb.message.answer(LOCALES[lang]["cmp_send_loc"])
    await cb.answer()

# ====== SHIKOYAT: Lokatsiya qabul qilish ======
@router.message(FeedbackFlow.waiting_location, F.location)
async def cmp_got_loc(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    loc = (message.location.latitude, message.location.longitude)
    await state.update_data(loc=loc)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(LOCALES[lang]["cmp_loc_ok"], reply_markup=complaint_actions_kb(lang))

# ====== SHIKOYAT: "Yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:csend")
async def cmp_send(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = LOCALES[lang]
    data = await state.get_data()
    text = data.get("text", "")
    photo_id = data.get("photo_id")
    loc = data.get("loc")

    # DB — oddiy feedback sifatida saqlaymiz (type yo'q, text mavjud)
    async with SessionLocal() as db:
        fb = await create_feedback(db, user_id=cb.from_user.id, text=text)
        # complaint_photo_id/complaint_location larni update qilish:
        if photo_id:
            from database.crud import attach_complaint_photo
            await attach_complaint_photo(db, fb.id, photo_id)
        if loc:
            from database.crud import attach_complaint_location
            await attach_complaint_location(db, fb.id, float(loc[0]), float(loc[1]))

        u = await get_user_by_tg(db, cb.from_user.id)

    # Guruhga yuborish (shikoyat ko‘k-qizil bilan)
    await _send_to_group_complaint(cb, lang, text, u, photo_id, loc)

    await state.clear()
    await cb.message.edit_text(t["cmp_sent"])
    await cb.message.answer(t["menu"], reply_markup=main_menu(lang))
    await cb.answer()

# ====== Yordamchi: guruhga yuborish formatlari ======
# def _fmt_user_block(lang: str, u) -> str:
#     t = LOCALES[lang]
#     # username may be None
#     username = f"@{u.username}" if getattr(u, "username", None) else "-"
#     return (
#         f"{t['grp_lang']}: {lang}\n"
#         f"{t['grp_user']}: {u.full_name or '-'} ({username})\n"
#         f"{t['grp_contact']}: {u.phone or '-'}\n"
#         f"{t['grp_age']}: {u.age or '-'}"
#     )

def _fmt_user_block(lang: str, u) -> str:
    from locales import LOCALES
    t = LOCALES.get(lang, LOCALES["uz"])
    grp_lang = t.get("grp_lang", "Language")  # ← default
    full_name = (u.full_name or "").strip()
    username  = f"@{u.username}" if u.username else "-"
    phone     = u.phone or "-"
    age       = str(u.age) if getattr(u, "age", None) is not None else "-"

    return (
        f"{grp_lang}: {lang}\n"
        f"👤 {full_name}\n"
        f"🪪 {username}\n"
        f"📞 {phone}\n"
        f"🔢 {age}\n"
    )


async def _send_to_group_review(message: Message, lang: str, rating: int, text: str, u):
    gid = int(getattr(settings, "GROUP_ID", 0) or 0)
    if not gid:
        return
    t = LOCALES[lang]
    tag = t["grp_tag_feedback"]  # 🟢
    block = _fmt_user_block(lang, u)
    caption = f"{tag} {t['grp_feedback']}\n\n{block}\n\n{t['grp_text']}: {text}\n{t['grp_rating']}: {rating}/5"
    try:
        await message.bot.send_message(gid, caption)
    except Exception:
        pass

async def _send_to_group_complaint(cb: CallbackQuery, lang: str, text: str, u, photo_id: str | None, loc: tuple | None):
    gid = int(getattr(settings, "GROUP_ID", 0) or 0)
    if not gid:
        return
    t = LOCALES[lang]
    tag = t["grp_tag_complaint"]  # 🔴
    block = _fmt_user_block(lang, u)
    caption = f"{tag} {t['grp_complaint']}\n\n{block}\n\n{t['grp_text']}: {text}"
    bot = cb.message.bot
    try:
        if photo_id:
            await bot.send_photo(gid, photo_id, caption=caption)
        else:
            await bot.send_message(gid, caption)
        if loc:
            lat, lon = loc
            await bot.send_location(gid, latitude=lat, longitude=lon)
    except Exception:
        pass
