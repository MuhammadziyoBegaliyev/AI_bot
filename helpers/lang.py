from database import SessionLocal
from database.crud import get_user_by_tg

async def get_lang(user_id: int) -> str:
    async with SessionLocal() as db:
        u = await get_user_by_tg(db, user_id)
        return u.lang if u else "uz"
