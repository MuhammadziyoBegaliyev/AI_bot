from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.feedback import FeedbackFlow
from locales import LOCALES
from database import SessionLocal
from database.crud import (
    create_feedback, set_feedback_rating,
    attach_complaint_photo, attach_complaint_location
)
from config import settings
from keyboards.inline import feedback_inline, back_kb
from filters.registered import RegisteredFilter
from utils.lang import get_lang
from sqlalchemy import select
from database.models import Feedback as FeedbackModel, User as UserModel

router = Router()

@router.message(RegisteredFilter(), F.text.in_({"💬 Fikr bildirish","💬 Feedback","💬 Отзыв"}))
async def ask_feedback(message: Message, state: FSMContext):
    # DB'dagi tanlangan tilni o'qiymiz
    lang = await get_lang(message.from_user.id)
    await state.clear()
    await state.set_state(FeedbackFlow.waiting_text)
    await message.answer(LOCALES[lang]["feedback_ask"])

@router.message(RegisteredFilter(), FeedbackFlow.waiting_text, F.text)
async def got_feedback(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    async with SessionLocal() as db:
        fb = await create_feedback(db, user_id=message.from_user.id, text=message.text)
    # Guruhga yuborish
    await message.bot.send_message(
        settings.GROUP_ID,
        f"💬 Feedback by @{message.from_user.username or '-'} (id={message.from_user.id})\n"
        f"Lang: {lang}\nText: {message.text}"
    )
    await message.answer(LOCALES[lang]["feedback_got"], reply_markup=feedback_inline(lang, fb.id))
    await state.clear()

@router.callback_query(RegisteredFilter(), F.data.startswith("rate:"))
async def rate_cb(cb: CallbackQuery):
    # callback: rate:<fb_id>:<rating>
    _, fb_id_str, rating_str = cb.data.split(":")
    fb_id, rating = int(fb_id_str), int(rating_str)

    async with SessionLocal() as db:
        fb = await set_feedback_rating(db, fb_id, rating)
        if not getattr(fb, "text", None):
            res = await db.execute(select(FeedbackModel).where(FeedbackModel.id == fb_id))
            fb = res.scalar_one()
        ures = await db.execute(select(UserModel).where(UserModel.id == fb.user_id))
        u = ures.scalar_one_or_none()

    lang = await get_lang(cb.from_user.id)
    await cb.message.answer(f"⭐ {rating}/5", reply_markup=back_kb(lang, "menu"))

    # Guruhga xabar
    uname = f"@{cb.from_user.username}" if cb.from_user.username else (u.full_name if u else str(cb.from_user.id))
    phone = (u.phone if u and u.phone else "-")
    link = (u.link if u and u.link else "-")
    txt = (
        "💬 Yangi fikr (baho bilan)\n"
        f"User: {uname} (tg_id={cb.from_user.id})\n"
        f"Telefon: {phone}\n"
        f"Link: {link}\n"
        f"Til: {lang}\n"
        f"⭐ Baho: {rating}/5\n"
        f"Matn: {fb.text}"
    )
    try:
        await cb.message.bot.send_message(settings.GROUP_ID, txt)
    except Exception:
        pass

    await cb.answer()

@router.callback_query(RegisteredFilter(), F.data.startswith("complain:"))
async def complaint_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    fb_id = int(cb.data.split(":")[1])
    await state.set_state(FeedbackFlow.waiting_complaint_text)
    await state.update_data(fb_id=fb_id)
    await cb.message.answer(LOCALES[lang]["complaint_ask"], reply_markup=back_kb(lang, "menu"))
    await cb.answer()

@router.message(RegisteredFilter(), FeedbackFlow.waiting_complaint_text, F.text)
async def complaint_text_ok(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    data = await state.get_data(); fb_id = data["fb_id"]
    await message.bot.send_message(
        settings.GROUP_ID,
        f"🚩 Complaint by @{message.from_user.username or '-'} (id={message.from_user.id})\n"
        f"Lang: {lang}\nText: {message.text}"
    )
    await state.set_state(FeedbackFlow.waiting_complaint_photo)
    await message.answer("Rasm yuboring (ixtiyoriy), yoki o'tkazish uchun matn yuboring.")

@router.message(RegisteredFilter(), FeedbackFlow.waiting_complaint_photo, F.photo)
async def complaint_photo_ok(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data(); fb_id = data["fb_id"]
    async with SessionLocal() as db:
        await attach_complaint_photo(db, fb_id, file_id)
    await message.answer("Rasm qabul qilindi. Lokatsiya yuborsangiz bo‘ladi (ixtiyoriy).")
    await state.set_state(FeedbackFlow.waiting_complaint_location)

@router.message(RegisteredFilter(), FeedbackFlow.waiting_complaint_photo, F.text)
async def complaint_photo_skip(message: Message, state: FSMContext):
    await message.answer("Rasm o'tkazib yuborildi. Lokatsiya yuborsangiz bo‘ladi (ixtiyoriy).")
    await state.set_state(FeedbackFlow.waiting_complaint_location)

@router.message(RegisteredFilter(), FeedbackFlow.waiting_complaint_location, F.location)
async def complaint_loc_ok(message: Message, state: FSMContext):
    data = await state.get_data(); fb_id = data["fb_id"]
    async with SessionLocal() as db:
        await attach_complaint_location(db, fb_id, message.location.latitude, message.location.longitude)
    await message.answer("Lokatsiya qabul qilindi. Rahmat!")
    await state.clear()

@router.message(RegisteredFilter(), FeedbackFlow.waiting_complaint_location, F.text)
async def complaint_loc_skip(message: Message, state: FSMContext):
    await message.answer("Lokatsiyasiz yakunlandi. Rahmat!")
    await state.clear()
