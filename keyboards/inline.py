from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales import LOCALES

def back_kb(lang: str, to: str = "menu") -> InlineKeyboardMarkup:
    """Universal 'Back' tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=LOCALES[lang]["back"], callback_data=f"back:{to}")]
        ]
    )

def drug_actions(lang: str, drug_id: int) -> InlineKeyboardMarkup:
    """Dori kartasi ostidagi tugmalar: doza kalkulyatori, yana qidirish, orqaga."""
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["dose_calc"], callback_data=f"dose:{drug_id}")],
            [InlineKeyboardButton(text=t["more_search"], callback_data="more_search")],
            [InlineKeyboardButton(text=t["back"], callback_data="back:search")],
        ]
    )

def feedback_inline(lang: str, fb_id: int) -> InlineKeyboardMarkup:
    """
    Fikr yuborilgach chiqadigan tugmalar:
    - 1..5 yulduzli baholash (callback: rate:{fb_id}:{1..5})
    - 🚩 Shikoyat / Complaint / Жалоба (callback: complain:{fb_id})
    - ⬅️ Orqaga (menu)
    """
    complaint_text = {
        "uz": "🚩 Shikoyat",
        "en": "🚩 Complaint",
        "ru": "🚩 Жалоба",
    }.get(lang, "🚩 Complaint")

    stars_row = [
        InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{fb_id}:{i}")
        for i in range(1, 6)
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            stars_row,
            [InlineKeyboardButton(text=complaint_text, callback_data=f"complain:{fb_id}")],
            [InlineKeyboardButton(text=LOCALES[lang]["back"], callback_data="back:menu")],
        ]
    )

# (ixtiyoriy) Lokatsiya bo‘limi uchun inline klaviaturalar
def locations_menu_inline(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["loc_btn_nearest"], callback_data="locmenu:nearest")],
            [InlineKeyboardButton(text=t["loc_btn_all"], callback_data="locmenu:all")],
            [InlineKeyboardButton(text=t["back"], callback_data="back:menu")],
        ]
    )

def locations_list_inline(lang: str, items: list) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    rows = []
    for loc in items:
        rows.append([InlineKeyboardButton(text=f"📍 {loc.title}", callback_data=f"locgo:{loc.id}")])
    rows.append([InlineKeyboardButton(text=t["loc_btn_nearest"], callback_data="locmenu:nearest")])
    rows.append([InlineKeyboardButton(text=t["back"], callback_data="back:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
