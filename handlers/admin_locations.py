from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import settings
from locales import LOCALES
from utils.lang import get_lang
from states.locations_admin import AddLocationFlow
from keyboards.inline import admin_panel_inline
from keyboards.reply import location_request_kb
from database import SessionLocal
from database.crud import add_pharmacy

router = Router()

def is_admin(user_id: int) -> bool:
    try:
        return user_id in settings.ADMIN_IDS
    except Exception:
        return False

# Admin panelga kirganda (sizda allaqachon /admin handler bo‘lishi mumkin)
@router.message(F.text.regexp(r"^/admin\b"))
async def open_admin(message: Message):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"]); return
    await message.answer("🛠", reply_markup=admin_panel_inline(lang))

# 1) Start: "➕ Lokatsiya qo‘shish"
@router.callback_query(F.data == "admin:add_location")
async def admin_add_location_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    if not is_admin(cb.from_user.id):
        await cb.message.answer(LOCALES[lang]["admin_only"]); await cb.answer(); return
    await state.set_state(AddLocationFlow.waiting_title)
    await cb.message.answer(LOCALES[lang]["admin_loc_title"])
    await cb.answer()

# 2) Title
@router.message(AddLocationFlow.waiting_title, F.text)
async def admin_loc_title(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"]); return
    await state.update_data(title=message.text.strip())
    await state.set_state(AddLocationFlow.waiting_address)
    await message.answer(LOCALES[lang]["admin_loc_address"])

# 3) Address
@router.message(AddLocationFlow.waiting_address, F.text)
async def admin_loc_address(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"]); return
    await state.update_data(address=message.text.strip())
    await state.set_state(AddLocationFlow.waiting_link)
    await message.answer(LOCALES[lang]["admin_loc_link"] + f' ({LOCALES[lang]["skip"]})')

# 4) Optional link
@router.message(AddLocationFlow.waiting_link, F.text)
async def admin_loc_link(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"]); return
    text = message.text.strip()
    link = None if text.lower() == LOCALES[lang]["skip"].lower() else text
    await state.update_data(link=link)
    await state.set_state(AddLocationFlow.waiting_point)
    await message.answer(LOCALES[lang]["admin_loc_ask_point"],
                         reply_markup=location_request_kb(lang))

# 5) Receive geo point and SAVE
@router.message(AddLocationFlow.waiting_point, F.location)
async def admin_loc_point(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(LOCALES[lang]["admin_only"]); return

    data = await state.get_data()
    lat = message.location.latitude
    lon = message.location.longitude
    async with SessionLocal() as db:
        await add_pharmacy(db,
                           title=data["title"],
                           address=data["address"],
                           link=data.get("link"),
                           lat=lat, lon=lon)

    await message.answer(LOCALES[lang]["admin_loc_saved"])
    await state.clear()
