# path: filters/registered.py
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database import SessionLocal
from database.crud import get_user_by_tg
from locales import LOCALES

class RegisteredFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        uid = event.from_user.id
        async with SessionLocal() as db:
            u = await get_user_by_tg(db, uid)
        if not u:
            try:
                await event.answer(LOCALES["uz"]["need_register"])
            except Exception:
                await event.message.answer(LOCALES["uz"]["need_register"])
            return False
        return True
