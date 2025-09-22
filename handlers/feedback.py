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


def tget(lang: str) -> dict:
    """Locale lug'atini xavfsiz qaytarish."""
    return LOCALES.get(lang, LOCALES["uz"])


# ====== KIRISH: "💬 Fikr bildirish" (main menu dan) ======
@router.message(
    RegisteredFilter(),
    F.text.in_({"💬 Fikr bildirish", "💬 Feedback", "💬 Отзыв"})
)
async def fb_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = tget(lang)
    await state.set_state(FeedbackFlow.choosing_type)
    await message.answer(t.get("fb_choose", "Iltimos, quyidagidan birini tanlang:"), reply_markup=fb_type_kb(lang))


# ====== TUR TANLASH: Fikr / Shikoyat ======
@router.callback_query(F.data.startswith("fb:type:"))
async def fb_choose_type(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = tget(lang)
    _, _, ftype = cb.data.split(":")
    if ftype == "review":
        # baho -> matn
        await state.set_state(FeedbackFlow.rating_wait)
        await cb.message.edit_text(
            t.get("fb_rate_ask", "Iltimos, baholang:"),
            reply_markup=fb_stars_kb(lang)
        )
    else:
        # shikoyat matni
        await state.set_state(FeedbackFlow.complaint_text)
        await cb.message.edit_text(
            t.get("cmp_ask_text", "Shikoyatingizni batafsil yozing:"),
            reply_markup=complaint_actions_kb(lang)
        )
    await cb.answer()


# ====== BAHO TANLASH (1..5) ======
@router.callback_query(F.data.startswith("fb:rate:"))
async def fb_rate(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = tget(lang)
    rating = int(cb.data.split(":")[2])
    await state.update_data(rating=rating)
    await state.set_state(FeedbackFlow.review_text)
    await cb.message.edit_text(t.get("fb_text_ask", "Fikringizni yozib yuboring:"))
    await cb.answer()


# ====== FIKR MATNI QABULI ======
@router.message(FeedbackFlow.review_text, F.text)
async def fb_got_review(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = tget(lang)
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
    await message.answer(t.get("fb_thanks", "Rahmat! Fikringiz qabul qilindi."), reply_markup=main_menu(lang))


# ====== SHIKOYAT MATNI QABULI ======
@router.message(FeedbackFlow.complaint_text, F.text)
async def cmp_got_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = tget(lang)
    await state.update_data(text=message.text.strip(), photo_id=None, loc=None)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(
        t.get("cmp_more", "Qo‘shimcha ma’lumot yuborishingiz mumkin: rasm yoki lokatsiya. Tayyor bo‘lsangiz “Yuborish”ni bosing."),
        reply_markup=complaint_actions_kb(lang)
    )


# ====== SHIKOYAT: "Rasm yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:cphoto")
async def cmp_want_photo(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = tget(lang)
    await state.set_state(FeedbackFlow.waiting_photo)
    await cb.message.answer(t.get("cmp_send_photo", "Rasm yuboring."))
    await cb.answer()


# ====== SHIKOYAT: Foydalanuvchi rasm yuboradi ======
@router.message(FeedbackFlow.waiting_photo, F.photo)
async def cmp_got_photo(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = tget(lang)
    file_id = message.photo[-1].file_id
    await state.update_data(photo_id=file_id)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(
        t.get("cmp_photo_ok", "Rasm qabul qilindi."),
        reply_markup=complaint_actions_kb(lang)
    )


# ====== SHIKOYAT: "Lokatsiyani yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:cloc")
async def cmp_want_loc(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = tget(lang)
    await state.set_state(FeedbackFlow.waiting_location)
    await cb.message.answer(t.get("cmp_send_loc", "Iltimos, lokatsiyangizni yuboring."))
    await cb.answer()


# ====== SHIKOYAT: Lokatsiya qabul qilish ======
@router.message(FeedbackFlow.waiting_location, F.location)
async def cmp_got_loc(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = tget(lang)
    loc = (message.location.latitude, message.location.longitude)
    await state.update_data(loc=loc)
    await state.set_state(FeedbackFlow.complaint_add)
    await message.answer(
        t.get("cmp_loc_ok", "Lokatsiya qabul qilindi."),
        reply_markup=complaint_actions_kb(lang)
    )


# ====== SHIKOYAT: "Yuborish" tugmasi ======
@router.callback_query(FeedbackFlow.complaint_add, F.data == "fb:csend")
async def cmp_send(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    t = tget(lang)
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

    # Guruhga yuborish (shikoyat)
    await _send_to_group_complaint(cb, lang, text, u, photo_id, loc)

    await state.clear()
    await cb.message.edit_text(t.get("cmp_sent", "Shikoyatingiz yuborildi. Rahmat!"))
    await cb.message.answer(t.get("menu", "Asosiy menyu:"), reply_markup=main_menu(lang))
    await cb.answer()


# ====== Yordamchi: guruhga yuborish formatlari ======
def _fmt_user_block(lang: str, u) -> str:
    t = tget(lang)
    grp_lang = t.get("grp_lang", "Language")
    full_name = (getattr(u, "full_name", "") or "").strip()
    username = f"@{u.username}" if getattr(u, "username", None) else "-"
    phone = getattr(u, "phone", None) or "-"
    age = str(getattr(u, "age", "")) if getattr(u, "age", None) is not None else "-"

    # Kalitlar bor-yo‘qligidan qat’i nazar, blok doim tuziladi
    lines = [
        f"{grp_lang}: {lang}",
        f"{t.get('grp_user', 'User')}: {full_name or '-'} ({username})",
        f"{t.get('grp_contact', 'Contact')}: {phone}",
        f"{t.get('grp_age', 'Age')}: {age}",
    ]
    return "\n".join(lines)


async def _send_to_group_review(message: Message, lang: str, rating: int, text: str, u):
    gid = int(getattr(settings, "GROUP_ID", 0) or 0)
    if not gid:
        return
    t = tget(lang)
    tag = t.get("grp_tag_feedback", "🟢 FEEDBACK")
    block = _fmt_user_block(lang, u)
    caption = (
        f"{tag}\n\n"
        f"{block}\n\n"
        f"{t.get('grp_text', 'Text')}: {text}\n"
        f"{t.get('grp_rating', 'Rating')}: {rating}/5"
    )
    try:
        await message.bot.send_message(gid, caption)
    except Exception:
        pass


async def _send_to_group_complaint(cb: CallbackQuery, lang: str, text: str, u, photo_id: str | None, loc: tuple | None):
    gid = int(getattr(settings, "GROUP_ID", 0) or 0)
    if not gid:
        return
    t = tget(lang)
    tag = t.get("grp_tag_complaint", "🔴 COMPLAINT")
    block = _fmt_user_block(lang, u)
    caption = (
        f"{tag}\n\n"
        f"{block}\n\n"
        f"{t.get('grp_text', 'Text')}: {text}"
    )
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
