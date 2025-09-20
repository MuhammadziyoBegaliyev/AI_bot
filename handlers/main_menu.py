from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.reply import main_menu, lang_kb
from locales import LOCALES
from database import SessionLocal
from database.crud import update_user_lang
from utils.lang import get_lang, set_lang_cache, clear_lang_cache
from filters.registered import RegisteredFilter

router = Router()

# 1) Menyuni ko'rsatish
@router.message(RegisteredFilter(), F.text.in_({"/menu", "/menyu"}))
@router.message(RegisteredFilter(), F.text.func(lambda s: s and s.lower() in {"menu", "menyu", "меню"}))
async def show_menu(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))

@router.callback_query(F.data == "back:menu")
async def back_to_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_lang(cb.from_user.id)
    await cb.message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))
    await cb.answer()

# 2) Tilni o'zgartirishni so'rash (har doim foydalanuvchi tilida)
@router.message(RegisteredFilter(), F.text.in_({"🌐 Tilni o'zgartirish","🌐 Change language","🌐 Сменить язык"}))
async def change_lang(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["choose_lang"], reply_markup=lang_kb())

@router.message(
    RegisteredFilter(),
    F.text.func(lambda s: s and s.replace("🌐", "").strip().lower() in {
        "tilni o'zgartirish", "change language", "сменить язык"
    })
)
async def change_lang_fuzzy(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["choose_lang"], reply_markup=lang_kb())

# 3) Tilni tanlash (UZ/EN/RU) — DB + cache
def _detect_code(btn_text: str) -> str:
    if btn_text.startswith("UZ"): return "uz"
    if btn_text.startswith("EN"): return "en"
    return "ru"

@router.message(RegisteredFilter(), F.text.in_({"UZ🇺🇿","EN🇬🇧","RU🇷🇺"}))
async def set_lang(message: Message, state: FSMContext):
    await state.clear()
    code = _detect_code(message.text)
    async with SessionLocal() as db:
        await update_user_lang(db, message.from_user.id, code)
    await clear_lang_cache(message.from_user.id)
    await set_lang_cache(message.from_user.id, code)
    await message.answer(LOCALES[code]["menu"], reply_markup=main_menu(code))

# 4) 'back:lang' bo'lsa — til tanlashga qaytarish
@router.callback_query(F.data == "back:lang")
async def back_to_lang(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_lang(cb.from_user.id)
    await cb.message.answer(LOCALES[lang]["choose_lang"], reply_markup=lang_kb())
    await cb.answer()










# from utils.lang import get_lang



# @router.message()
# async def fallback(message: Message):
#     lang = await get_lang(message.from_user.id)
#     await message.answer(LOCALES[lang]["menu"])
