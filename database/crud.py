# path: database/crud.py
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Drug, Pharmacy, SearchLog, Feedback, Location

# =====================================
# USERS
# =====================================
async def get_user_by_tg(db: AsyncSession, tg_id: int):
    q = await db.execute(select(User).where(User.tg_id == tg_id))
    return q.scalar_one_or_none()

async def upsert_user(
    db: AsyncSession,
    tg_id: int,
    username: str | None,
    link: str | None,
    full_name: str,
    phone: str,
    age: int,
    lang: str,
):
    u = await get_user_by_tg(db, tg_id)
    if u:
        u.username = username
        u.link = link
        u.full_name = full_name
        u.phone = phone
        u.age = age
        u.lang = lang
    else:
        u = User(
            tg_id=tg_id,
            username=username,
            link=link,
            full_name=full_name,
            phone=phone,
            age=age,
            lang=lang,
        )
        db.add(u)
    await db.flush()
    await db.commit()
    return u

async def update_user_lang(db: AsyncSession, tg_id: int, lang: str):
    u = await get_user_by_tg(db, tg_id)
    if u:
        u.lang = lang
    else:
        # foydalanuvchi hali yaratilmagan bo‘lsa ham tilni yozib qo‘yish
        u = User(tg_id=tg_id, username=None, link=None, full_name="", phone="", age=0, lang=lang)
        db.add(u)
    await db.flush()
    await db.commit()
    return u

# =====================================
# DRUGS
# =====================================
async def add_drug(db: AsyncSession, **kwargs):
    # title -> name map (eski oqimdan kelgan bo‘lishi mumkin)
    if "title" in kwargs and "name" not in kwargs:
        kwargs["name"] = kwargs.pop("title")

    # narxlarni float ga aylantirish
    for k in ("price_min", "price_max"):
        if k in kwargs and kwargs[k] is not None:
            try:
                kwargs[k] = float(str(kwargs[k]).replace(",", "."))
            except Exception:
                kwargs[k] = None

    d = Drug(**kwargs)
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d

async def list_drugs(db: AsyncSession, limit: int = 50):
    q = await db.execute(select(Drug).order_by(Drug.name).limit(limit))
    return q.scalars().all()

async def delete_drug(db: AsyncSession, drug_id: int):
    await db.execute(delete(Drug).where(Drug.id == drug_id))
    await db.commit()

async def find_drug_by_name(db: AsyncSession, name: str):
    q = await db.execute(select(Drug).where(Drug.name.ilike(f"%{name}%")))
    return q.scalars().all()

# =====================================
# PHARMACIES
# =====================================
async def add_pharmacy(db: AsyncSession, **kwargs):
    # lat/lon string bo‘lsa, floatga aylantiramiz
    for k in ("lat", "lon"):
        if k in kwargs and kwargs[k] is not None:
            try:
                kwargs[k] = float(str(kwargs[k]).replace(",", "."))
            except Exception:
                kwargs[k] = None

    p = Pharmacy(**kwargs)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p

async def list_pharmacies(db: AsyncSession, limit: int = 100):
    q = await db.execute(select(Pharmacy).order_by(Pharmacy.title).limit(limit))
    return q.scalars().all()

async def delete_pharmacy(db: AsyncSession, pid: int):
    await db.execute(delete(Pharmacy).where(Pharmacy.id == pid))
    await db.commit()

async def all_pharmacies(db: AsyncSession):
    q = await db.execute(select(Pharmacy))
    return q.scalars().all()

# =====================================
# LOGS & FEEDBACK
# =====================================
async def log_search(db: AsyncSession, user_id: int, term: str):
    db.add(SearchLog(user_id=user_id, term=term))
    await db.commit()

async def top_searches(db: AsyncSession, limit: int = 10):
    q = await db.execute(
        select(SearchLog.term, func.count().label("cnt"))
        .group_by(SearchLog.term)
        .order_by(func.count().desc())
        .limit(limit)
    )
    return q.all()

async def create_feedback(db: AsyncSession, user_id: int, text: str):
    fb = Feedback(user_id=user_id, text=text)
    db.add(fb)
    await db.commit()
    return fb

async def set_feedback_rating(db: AsyncSession, fb_id: int, rating: int):
    q = await db.execute(select(Feedback).where(Feedback.id == fb_id))
    fb = q.scalar_one()
    fb.rating = rating
    await db.commit()
    return fb

async def attach_complaint_photo(db: AsyncSession, fb_id: int, file_id: str):
    q = await db.execute(select(Feedback).where(Feedback.id == fb_id))
    fb = q.scalar_one()
    fb.complaint_photo_id = file_id
    await db.commit()

async def attach_complaint_location(db: AsyncSession, fb_id: int, lat: float, lon: float):
    q = await db.execute(select(Feedback).where(Feedback.id == fb_id))
    fb = q.scalar_one()
    fb.complaint_location = f"{lat},{lon}"
    await db.commit()

async def list_feedbacks(db: AsyncSession, limit: int = 20):
    q = await db.execute(select(Feedback).order_by(Feedback.created_at.desc()).limit(limit))
    return q.scalars().all()

# =====================================
# LOCATIONS (foydalanuvchi ko‘radigan bo‘lim uchun)
# =====================================
async def add_location(
    db: AsyncSession, *, title: str, address: str, lat: float, lon: float, link: str | None = None
):
    loc = Location(title=title, address=address, lat=lat, lon=lon, link=link)
    db.add(loc)
    await db.commit()
    await db.refresh(loc)
    return loc

async def list_locations(db: AsyncSession, limit: int = 4):
    q = await db.execute(select(Location).limit(limit))
    return q.scalars().all()

async def get_location(db: AsyncSession, loc_id: int):
    q = await db.execute(select(Location).where(Location.id == loc_id))
    return q.scalar_one_or_none()

async def delete_location(db: AsyncSession, loc_id: int):
    await db.execute(delete(Location).where(Location.id == loc_id))
    await db.commit()



async def get_all_user_ids(db) -> list[int]:
    res = await db.execute(select(User.tg_id))
    return [row[0] for row in res.all()]


# path: database/crud.py
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError, OperationalError

# Agar allaqachon bo'lsa, takror qo'shmang:
try:
    from .models import User
except Exception:
    User = None

try:
    from .models import Feedback
except Exception:
    Feedback = None


async def list_all_users(db) -> list[tuple[int]]:
    """
    Barcha foydalanuvchi Telegram ID larini qaytaradi.
    Format: [(tg_id,), (tg_id,), ...] — handlers/admin.py shu shaklni qo'llab turadi.
    Avval User jadvali, bo'lmasa Feedback dan distinct user_id olamiz.
    """
    # 1) User jadvali bor bo'lsa, undan o'qish:
    if User is not None and hasattr(User, "tg_id"):
        try:
            res = await db.execute(select(User.tg_id))
            rows = res.all()
            return [(r[0],) for r in rows if r[0] is not None]
        except (ProgrammingError, OperationalError):
            pass  # pastdagi fallback'ga o'tamiz

    # 2) Fallback: Feedback jadvalidagi noyob user_id lar
    if Feedback is not None and hasattr(Feedback, "user_id"):
        res = await db.execute(select(Feedback.user_id).distinct())
        rows = res.all()
        return [(r[0],) for r in rows if r[0] is not None]

    # 3) Oxirgi chora — hech narsa topilmasa bo'sh ro'yxat
    return []





# Foydalanuvchi bo‘yicha qidiruvlar (so‘nggi tartibda)
async def get_user_searches(db, tg_id: int) -> list[str]:
    try:
        from .models import SearchQuery  # model nomi siznikida boshqacha bo‘lsa moslang
    except Exception:
        return []
    q = await db.execute(
        select(SearchQuery.query)
        .where(SearchQuery.user_id == tg_id)
        .order_by(SearchQuery.created_at.desc())
        .limit(10)
    )
    return [r[0] for r in q.all()]

# Foydalanuvchi feedback/complaintlari
async def get_user_feedbacks(db, tg_id: int):
    try:
        from .models import Feedback
    except Exception:
        return []
    q = await db.execute(select(Feedback).where(Feedback.user_id == tg_id))
    return [row[0] for row in q.all()]
