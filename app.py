
import asyncio
import logging
import signal
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database import init_db

# Routers
from handlers.start import router as start_router
from handlers.register import router as register_router
from handlers.main_menu import router as menu_router
from handlers.search import router as search_router
from handlers.feedback import router as fb_router
from handlers.locations import router as locations_router
from handlers.admin import router as admin_router
from handlers.admin_panel import router as admin_panel_router
from handlers.ai_chat import router as ai_router

log = logging.getLogger("farmastevtika.app")


async def on_shutdown(dp: Dispatcher, bot: Bot) -> None:
    """Graceful shutdown: storage & HTTP session."""
    log.info("Shutting down dispatcher…")

    # Storage (MemoryStorage uchun maxsus yopish shart emas, lekin bor bo'lsa chaqiramiz)
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


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


async def _run() -> None:
    _setup_logging()

    # Konfiguratsiya bo‘yicha bir nechta foydali loglar
    if not settings.BOT_TOKEN:
        log.error("BOT_TOKEN bo'sh! .env faylini tekshiring.")
        return
    if not settings.DATABASE_URL:
        log.warning("DATABASE_URL bo'sh — default ishlatiladi.")

    # DB
    log.info("Initializing database…")
    await init_db()
    log.info("Database ready.")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Aiogram v3: storage sozlash
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlar tartibi:
    # 1) Admin & boshqaruv
    dp.include_router(admin_router)
    dp.include_router(admin_panel_router)

    # 2) Start/ro'yxat/ menyu
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(menu_router)

    # 3) Asosiy funksiyalar
    dp.include_router(search_router)
    dp.include_router(locations_router)
    dp.include_router(fb_router)
    dp.include_router(ai_router)

    # Signal'lar: Ctrl+C va OS signalida toza yopilish
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(dp.stop_polling()))

    log.info("Bot polling started.")
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(dp, bot)


if __name__ == "__main__":
    asyncio.run(_run())
