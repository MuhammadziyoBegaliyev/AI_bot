# path: database/models.py
from sqlalchemy import BigInteger, Integer, String, Float, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from . import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    link: Mapped[str | None] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(32))
    age: Mapped[int] = mapped_column(Integer)
    lang: Mapped[str] = mapped_column(String(2), default="uz")

class Drug(Base):
    __tablename__ = "drugs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    uses: Mapped[str] = mapped_column(Text)
    side_effects: Mapped[str] = mapped_column(Text)
    dosage: Mapped[str] = mapped_column(Text)
    price_min: Mapped[float] = mapped_column(Float, default=0)
    price_max: Mapped[float] = mapped_column(Float, default=0)
    call_center: Mapped[str | None] = mapped_column(String(32))
    alternatives: Mapped[str | None] = mapped_column(Text)

class Pharmacy(Base):
    __tablename__ = "pharmacies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128))
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    address: Mapped[str] = mapped_column(String(256))
    phone: Mapped[str | None] = mapped_column(String(32))

class SearchLog(Base):
    __tablename__ = "search_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    term: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedbacks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)
    rating: Mapped[int | None] = mapped_column(Integer)
    complaint_photo_id: Mapped[str | None] = mapped_column(String(256))
    complaint_location: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())





class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)   # filial nomi
    address: Mapped[str] = mapped_column(String(255), nullable=False) # manzil matni
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=True)     # xarita URL (ixtiyoriy)
