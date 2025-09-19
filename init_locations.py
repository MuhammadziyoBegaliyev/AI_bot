import asyncio
from database import SessionLocal, init_db
from database.crud import add_pharmacy

DEFAULT_LOCATIONS = [
    {
        "title": "Chilonzor apteka",
        "address": "Toshkent, Chilonzor tumani",
        "link": "https://maps.google.com/?q=41.285,69.203",
        "lat": 41.285,
        "lon": 69.203,
    },
    {
        "title": "Yunusobod apteka",
        "address": "Toshkent, Yunusobod tumani",
        "link": "https://maps.google.com/?q=41.356,69.285",
        "lat": 41.356,
        "lon": 69.285,
    },
    {
        "title": "Sergeli apteka",
        "address": "Toshkent, Sergeli tumani",
        "link": "https://maps.google.com/?q=41.216,69.212",
        "lat": 41.216,
        "lon": 69.212,
    },
    {
        "title": "Olmazor apteka",
        "address": "Toshkent, Olmazor tumani",
        "link": "https://maps.google.com/?q=41.338,69.239",
        "lat": 41.338,
        "lon": 69.239,
    },
]

async def seed():
   
    await init_db()
    async with SessionLocal() as db:
        for loc in DEFAULT_LOCATIONS:
            await add_pharmacy(db, **loc)
        print(f"✅ {len(DEFAULT_LOCATIONS)} ta lokatsiya qo'shildi.")

if __name__ == "__main__":
    asyncio.run(seed())
