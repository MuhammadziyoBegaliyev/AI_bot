from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from locales import LOCALES

def main_menu(lang: str) -> ReplyKeyboardMarkup:
    t = LOCALES[lang]
    kb = [
        [KeyboardButton(text=t["btn_search"])],
        [KeyboardButton(text=t["btn_feedback"])],
        [KeyboardButton(text=t["btn_locations"])],   # ➕ Lokatsiyalar tugmasi
        [KeyboardButton(text=t["btn_ai"])],  # ➕ Sun'iy intellekt tugmasi
        [KeyboardButton(text=t["btn_lang"])],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def lang_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="UZ🇺🇿"), KeyboardButton(text="EN🇬🇧"), KeyboardButton(text="RU🇷🇺")]]
    )

# Foydalanuvchidan hozirgi joylashuvni so‘rash uchun (eng yaqin lokatsiya oqimida)
def location_request_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=LOCALES[lang]["ask_share_button"], request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def ai_chat_kb(lang: str) -> ReplyKeyboardMarkup:
    """AI rejimi uchun sodda klaviatura: faqat orqaga."""
    t = LOCALES[lang]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=t["back"])]]
    )