# path: app.py
import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # default storage (wait_closed yo'q)

from config import settings
from database import init_db

# Routers
from handlers.start import router as start_router
from handlers.register import router as register_router
from handlers.main_menu import router as menu_router
from handlers.search import router as search_router
from handlers.feedback import router as fb_router
from handlers.admin import router as admin_router
from handlers.locations import router as locations_router
from handlers.admin_panel import router as admin_panel_router
from handlers.ai_chat import router as ai_router

log = logging.getLogger("farmastevtika.app")


async def on_shutdown(dp: Dispatcher, bot: Bot) -> None:
    """Graceful shutdown: storage & HTTP session."""
    log.info("Shutting down dispatcher…")

    # Storage'ni muloyim yopish (MemoryStorage uchun hech narsa shart emas)
    storage = getattr(dp, "storage", None)
    if storage is not None:
        close = getattr(storage, "close", None)
        if callable(close):
            with suppress(Exception):
                await close()
        wait_closed = getattr(storage, "wait_closed", None)
        if callable(wait_closed):
            with suppress(Exception):
                await wait_closed()

    # Bot HTTP sessiyasini yopish
    with suppress(Exception):
        await bot.session.close()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    log.info("Initializing database…")
    await init_db()
    log.info("Database ready.")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Aiogram v3: storage ni istasangiz Redis bilan almashtirasiz
    dp = Dispatcher(storage=MemoryStorage())

    # Routers
    dp.include_router(admin_router)
    dp.include_router(admin_panel_router)
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(menu_router)
    dp.include_router(search_router)
    dp.include_router(fb_router)   
    dp.include_router(locations_router)
    dp.include_router(ai_router) 

    log.info("Bot polling started.")
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
