# path: handlers/admin_broadcast.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config import settings
from utils.lang import get_lang
from locales import LOCALES
from states.admin_broadcast import AdminBroadcast
from keyboards.inline import bc_yes_no_photo_kb, bc_preview_kb
from keyboards.reply import main_menu
from database import SessionLocal
from database.crud import get_all_user_ids

router = Router()

def _is_admin(user_id: int) -> bool:
    try:
        admins = set(int(x) for x in getattr(settings, "ADMINS", []))
    except Exception:
        admins = set()
    return user_id in admins

# --- Kirish: admin paneldan tugmalar ---
@router.callback_query(F.data.in_({"adm:bc:promo","adm:bc:msg"}))
async def bc_start(cb: CallbackQuery, state: FSMContext):
    if not _is_admin(cb.from_user.id):
        await cb.answer("Admins only", show_alert=True)
        return
    lang = await get_lang(cb.from_user.id)
    mode = "promo" if cb.data.endswith("promo") else "msg"
    await state.set_state(AdminBroadcast.ask_photo)
    await state.update_data(mode=mode, photo_id=None, text=None)
    await cb.message.edit_text(LOCALES[lang]["adm_bc_want_photo"], reply_markup=bc_yes_no_photo_kb(lang))
    await cb.answer()

# --- Rasm xohlash/xohlamaslik ---
@router.callback_query(AdminBroadcast.ask_photo, F.data.startswith("bc:want:"))
async def bc_want_photo(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    yn = cb.data.split(":")[-1]
    if yn == "yes":
        await state.set_state(AdminBroadcast.waiting_photo)
        await cb.message.edit_text(LOCALES[lang]["adm_bc_send_photo"])
    else:
        await state.set_state(AdminBroadcast.waiting_text)
        await cb.message.edit_text(LOCALES[lang]["adm_bc_ask_text"])
    await cb.answer()

# --- Rasm qabul qilish ---
@router.message(AdminBroadcast.waiting_photo, F.photo)
async def bc_got_photo(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    file_id = message.photo[-1].file_id
    await state.update_data(photo_id=file_id)
    await state.set_state(AdminBroadcast.waiting_text)
    await message.answer(LOCALES[lang]["adm_bc_photo_ok"])
    await message.answer(LOCALES[lang]["adm_bc_ask_text"])

# --- Matn qabul qilish ---
@router.message(AdminBroadcast.waiting_text, F.text)
async def bc_got_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    data = await state.get_data()
    await state.update_data(text=message.text.strip())

    # Oldindan ko‘rish
    t = LOCALES[lang]
    await state.set_state(AdminBroadcast.preview)
    photo_id = data.get("photo_id")
    if photo_id:
        await message.answer_photo(photo=photo_id, caption=f"{t['adm_bc_preview_title']}\n\n{message.text}", reply_markup=bc_preview_kb(lang))
    else:
        await message.answer(f"{t['adm_bc_preview_title']}\n\n{message.text}", reply_markup=bc_preview_kb(lang))

# --- Tahrirlash tugmalari ---
@router.callback_query(AdminBroadcast.preview, F.data == "bc:edit:text")
async def bc_edit_text(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(AdminBroadcast.waiting_text)
    await cb.message.answer(LOCALES[lang]["adm_bc_ask_text"])
    await cb.answer()

@router.callback_query(AdminBroadcast.preview, F.data == "bc:edit:photo")
async def bc_edit_photo(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(AdminBroadcast.waiting_photo)
    await cb.message.answer(LOCALES[lang]["adm_bc_send_photo"])
    await cb.answer()

@router.callback_query(AdminBroadcast.preview, F.data == "bc:cancel")
async def bc_cancel(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.clear()
    await cb.message.edit_text(LOCALES[lang]["adm_bc_cancelled"], reply_markup=main_menu(lang))
    await cb.answer()

# --- Yuborish ---
@router.callback_query(AdminBroadcast.preview, F.data == "bc:send")
async def bc_send_all(cb: CallbackQuery, state: FSMContext):
    if not _is_admin(cb.from_user.id):
        await cb.answer("Admins only", show_alert=True)
        return
    lang = await get_lang(cb.from_user.id)
    t = LOCALES[lang]
    data = await state.get_data()
    text = data.get("text", "")
    photo_id = data.get("photo_id")

    await cb.message.edit_text(t["adm_bc_sending"])

    # Barcha foydalanuvchilarga jo‘natish
    sent, fail = 0, 0
    async with SessionLocal() as db:
        user_ids = await get_all_user_ids(db)

    bot = cb.message.bot
    for uid in user_ids:
        try:
            if photo_id:
                await bot.send_photo(uid, photo_id, caption=text)
            else:
                await bot.send_message(uid, text)
            sent += 1
        except Exception:
            fail += 1
            continue

    await state.clear()
    await cb.message.edit_text(f"{t['adm_bc_done']} ({sent} OK, {fail} fail)", reply_markup=main_menu(lang))
    await cb.answer()
