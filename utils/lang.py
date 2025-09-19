from database import SessionLocal
from database.crud import get_user_by_tg

LANG_CACHE: dict[int, str] = {}

async def get_lang(user_id: int) -> str:
    code = LANG_CACHE.get(user_id)
    if code:
        return code
    async with SessionLocal() as db:
        u = await get_user_by_tg(db, user_id)
        code = (u.lang if u and u.lang else "uz")
    LANG_CACHE[user_id] = code
    return code

async def set_lang_cache(user_id: int, code: str) -> None:
    LANG_CACHE[user_id] = code

async def clear_lang_cache(user_id: int | None = None) -> None:
    if user_id is None:
        LANG_CACHE.clear()
    else:
        LANG_CACHE.pop(user_id, None)
