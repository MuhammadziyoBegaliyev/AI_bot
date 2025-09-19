# path: handlers/register.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, Contact
from aiogram.fsm.context import FSMContext
from locales import LOCALES
from states.register import Register
from database import SessionLocal
from database.crud import upsert_user
from keyboards.reply import main_menu
import re

router = Router()

def back_kb(lang): 
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text=LOCALES[lang]["back"])]])

def contact_kb(lang):
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="📱 Share Contact", request_contact=True)],
        [KeyboardButton(text=LOCALES[lang]["back"])]
    ])

@router.message(Register.waiting_name, F.text)
async def reg_name(message: Message, state: FSMContext):
    data = await state.get_data(); lang = data.get("tmp_lang","uz")
    full_name = message.text.strip()
    if len(full_name) < 3:
        await message.answer("Ism-familya juda qisqa. Qayta yuboring.", reply_markup=back_kb(lang)); return
    await state.update_data(full_name=full_name)
    await state.set_state(Register.waiting_contact)
    await message.answer(LOCALES[lang]["reg_contact"], reply_markup=contact_kb(lang))

@router.message(Register.waiting_contact, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    data = await state.get_data(); lang = data.get("tmp_lang","uz")
    assert isinstance(message.contact, Contact)
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.waiting_age)
    await message.answer(LOCALES[lang]["reg_age"], reply_markup=back_kb(lang))

@router.message(Register.waiting_contact, F.text)
async def reg_contact_text(message: Message, state: FSMContext):
    data = await state.get_data(); lang = data.get("tmp_lang","uz")
    if message.text == LOCALES[lang]["back"]:
        await state.set_state(Register.waiting_name); await message.answer(LOCALES[lang]["reg_name"]); return
    digits = re.sub(r"\D", "", message.text)
    if len(digits) < 9:
        await message.answer("Telefonni to‘g‘ri kiriting yoki 'Share Contact' bosing.", reply_markup=contact_kb(lang)); return
    await state.update_data(phone=digits)
    await state.set_state(Register.waiting_age)
    await message.answer(LOCALES[lang]["reg_age"], reply_markup=back_kb(lang))

@router.message(Register.waiting_age, F.text.regexp(r"^\d{1,3}$"))
async def reg_age(message: Message, state: FSMContext):
    data = await state.get_data(); lang = data.get("tmp_lang","uz"); age = int(message.text)
    if age <= 0 or age > 120:
        await message.answer("Yosh noto‘g‘ri. Qayta kiriting.", reply_markup=back_kb(lang)); return
    link = f"https://t.me/{message.from_user.username}" if message.from_user.username else None
    async with SessionLocal() as db:
        await upsert_user(db,
            tg_id=message.from_user.id,
            username=message.from_user.username,
            link=link,
            full_name=data["full_name"],
            phone=data["phone"],
            age=age,
            lang=lang
        )
    await state.clear()
    await message.answer(LOCALES[lang]["reg_done"], reply_markup=main_menu(lang))

@router.message(Register.waiting_age, F.text)
async def reg_age_any(message: Message, state: FSMContext):
    data = await state.get_data(); lang = data.get("tmp_lang","uz")
    if message.text == LOCALES[lang]["back"]:
        await state.set_state(Register.waiting_contact)
        await message.answer(LOCALES[lang]["reg_contact"], reply_markup=contact_kb(lang)); return
    await message.answer("Faqat raqam kiriting (masalan: 23).", reply_markup=back_kb(lang))
