# path: config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: tuple[int, ...] = tuple(int(x.strip()) for x in os.getenv("ADMIN_IDS","").split(",") if x.strip())
    GROUP_ID: int = int(os.getenv("GROUP_ID", "0"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///pharma.db")

settings = Settings()
