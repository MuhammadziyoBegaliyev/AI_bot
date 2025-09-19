from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from keyboards.reply import lang_kb, main_menu
from database import SessionLocal
from database.crud import get_user_by_tg, update_user_lang
from states.register import Register
from utils.lang import get_lang, set_lang_cache, clear_lang_cache

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    # Foydalanuvchining hozirgi (DB yoki default) tilida kutib olish
    lang = await get_lang(message.from_user.id)
    await message.answer(
        LOCALES[lang]["welcome"] + "\n" + LOCALES[lang]["choose_lang"],
        reply_markup=lang_kb()
    )

@router.message(F.text.in_({"UZ🇺🇿", "EN🇬🇧", "RU🇷🇺"}))
async def choose_lang(message: Message, state: FSMContext):
    code = "uz" if message.text.startswith("UZ") else ("en" if message.text.startswith("EN") else "ru")

    async with SessionLocal() as db:
        u = await get_user_by_tg(db, message.from_user.id)
        if u:
            # mavjud user — DB va cache ni yangilaymiz
            await update_user_lang(db, message.from_user.id, code)
            await clear_lang_cache(message.from_user.id)
            await set_lang_cache(message.from_user.id, code)
            await message.answer(LOCALES[code]["menu"], reply_markup=main_menu(code))
        else:
            # yangi user — ro'yxatdan o'tish oqimi, lekin cache ni darhol sozlaymiz
            await clear_lang_cache(message.from_user.id)
            await set_lang_cache(message.from_user.id, code)
            await state.set_state(Register.waiting_name)
            await state.update_data(tmp_lang=code)
            await message.answer(LOCALES[code]["reg_name"])
