# path: handlers/locations.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from filters.registered import RegisteredFilter
from utils.lang import get_lang
from keyboards.inline import locations_menu_inline, locations_list_inline
from keyboards.reply import location_request_kb
from database import SessionLocal
from database.crud import list_locations, get_location
from utils.geo import nearest
from states.locations import LocationsFlow

router = Router()

# 1) Asosiy menyudan "📍 Lokatsiyalar" bosilganda
@router.message(RegisteredFilter(), F.text.in_({"📍 Lokatsiyalar", "📍 Locations", "📍 Локации"}))
async def show_locations_menu(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(
        LOCALES[lang]["loc_menu_title"],
        reply_markup=locations_menu_inline(lang)
    )

# 2) "Hamma lokatsiyalar"
@router.callback_query(F.data == "locmenu:all")
async def list_all_locations(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    async with SessionLocal() as db:
        locs = await list_locations(db, limit=4)

    if not locs:
        await cb.message.answer(LOCALES[lang]["no_locations"])
        await cb.answer()
        return

    lines = [LOCALES[lang]["loc_list_title"]]
    for i, loc in enumerate(locs, start=1):
        url = loc.link or f"https://maps.google.com/?q={loc.lat},{loc.lon}"
        lines.append(f'{i}) <a href="{url}">{loc.title}</a> — {loc.address}')
    lines.append("")
    lines.append(LOCALES[lang]["choose_or_nearest"])

    await cb.message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=locations_list_inline(lang, locs),
    )
    await cb.answer()

# 3) Ro'yxatdan aniq lokatsiyani tanlash
@router.callback_query(F.data.startswith("locgo:"))
async def go_to_location(cb: CallbackQuery):
    lang = await get_lang(cb.from_user.id)
    loc_id = int(cb.data.split(":")[1])

    async with SessionLocal() as db:
        loc = await get_location(db, loc_id)

    if not loc:
        await cb.message.answer(LOCALES[lang]["no_locations"])
        await cb.answer()
        return

    await cb.message.answer_location(latitude=loc.lat, longitude=loc.lon)
    await cb.message.answer(
        LOCALES[lang]["loc_sent_caption"].format(title=loc.title, address=loc.address)
    )
    await cb.answer()

# 4) "Eng yaqin lokatsiya" -> lokatsiya so'rash
@router.callback_query(F.data == "locmenu:nearest")
async def ask_user_location(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(cb.from_user.id)
    await state.set_state(LocationsFlow.waiting_user_location)
    await cb.message.answer(LOCALES[lang]["ask_share_loc"], reply_markup=location_request_kb(lang))
    await cb.answer()

# 5) Foydalanuvchi lokatsiya yuborganda
@router.message(RegisteredFilter(), LocationsFlow.waiting_user_location, F.location)
async def show_nearest(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)

    async with SessionLocal() as db:
        locs = await list_locations(db, limit=4)

    if not locs:
        await message.answer(LOCALES[lang]["no_locations"])
        await state.clear()
        return

    items = [(loc.id, loc.title, loc.lat, loc.lon) for loc in locs]
    (loc_id, title, lat, lon), dist = nearest(
        message.location.latitude, message.location.longitude, items
    )

    await message.answer(f"{LOCALES[lang]['nearest_prefix']} {title}")
    await message.answer_location(latitude=lat, longitude=lon)

    found = next((l for l in locs if l.id == loc_id), None)
    if found:
        await message.answer(
            LOCALES[lang]["loc_sent_caption"].format(title=found.title, address=found.address)
        )

    await state.clear()
