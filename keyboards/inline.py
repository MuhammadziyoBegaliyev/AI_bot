# path: keyboards/inline.py
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
    """
    Dori kartasi ostidagi tugmalar: doza kalkulyatori, yana qidirish, orqaga.
    """
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["dose_calc"], callback_data=f"dose:{drug_id}")],
            [InlineKeyboardButton(text=t["more_search"], callback_data="more_search")],
            [InlineKeyboardButton(text=t["back"], callback_data="back:search")],
        ]
    )


# ===============================
#  FIKR / SHIKOYAT OQIMI (YANGI)
# ===============================
def fb_type_kb(lang: str) -> InlineKeyboardMarkup:
    """
    Foydalanuvchi 'Fikr bildirish' bo'limiga kirganda tur tanlash:
    - 🟩 Fikr bildirish
    - 🟥 Shikoyat qilish
    """
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["fb_btn_feedback"], callback_data="fb:type:review")],
            [InlineKeyboardButton(text=t["fb_btn_complaint"], callback_data="fb:type:complaint")],
            [InlineKeyboardButton(text=t["back"], callback_data="back:menu")],
        ]
    )


def fb_stars_kb(lang: str) -> InlineKeyboardMarkup:
    """
    5 yulduzli baholash – 3 ta yuqorida, 2 ta pastda (sig‘ishi uchun).
    callback: fb:rate:{1..5}
    """
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐️ 1", callback_data="fb:rate:1"),
                InlineKeyboardButton(text="⭐️ 2", callback_data="fb:rate:2"),
                InlineKeyboardButton(text="⭐️ 3", callback_data="fb:rate:3"),
            ],
            [
                InlineKeyboardButton(text="⭐️ 4", callback_data="fb:rate:4"),
                InlineKeyboardButton(text="⭐️ 5", callback_data="fb:rate:5"),
            ],
            [InlineKeyboardButton(text=t["back"], callback_data="back:menu")],
        ]
    )


def complaint_actions_kb(lang: str) -> InlineKeyboardMarkup:
    """
    Shikoyat matnidan keyingi tugmalar:
    - 📷 Rasm yuborish (fb:cphoto)
    - 📍 Lokatsiyani yuborish (fb:cloc)
    - ✅ Shikoyatni yuborish (fb:csend)
    """
    t = LOCALES[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t["cmp_btn_photo"], callback_data="fb:cphoto"),
                InlineKeyboardButton(text=t["cmp_btn_loc"], callback_data="fb:cloc"),
            ],
            [InlineKeyboardButton(text=t["cmp_btn_send"], callback_data="fb:csend")],
            [InlineKeyboardButton(text=t["back"], callback_data="back:menu")],
        ]
    )


# (ESKI, agar boshqa joylarda ishlatilayotgan bo‘lsa — qolsin)
def feedback_inline(lang: str, fb_id: int) -> InlineKeyboardMarkup:
    """
    Legacy: Fikr yuborilgach chiqadigan tugmalar (yulduzlar bitta qatorda).
    Hozir yangi oqimdan foydalanamiz (fb_stars_kb), lekin bu funksiya
    orqaga moslik uchun saqlab qo'yildi.
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


# ===============================
#  LOKATSIYALAR BO'LIMI
# ===============================
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
        rows.append(
            [InlineKeyboardButton(text=f"📍 {loc.title}", callback_data=f"locgo:{loc.id}")]
        )
    rows.append([InlineKeyboardButton(text=t["loc_btn_nearest"], callback_data="locmenu:nearest")])
    rows.append([InlineKeyboardButton(text=t["back"], callback_data="back:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)





def admin_main_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    # Mavjud admin tugmalaringiz bo‘lsa, shular bilan BIR qatorda foydalaning.
    rows = [
        [InlineKeyboardButton(text=t["adm_btn_send_promo"], callback_data="adm:bc:promo")],
        [InlineKeyboardButton(text=t["adm_btn_send_msg"], callback_data="adm:bc:msg")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def bc_yes_no_photo_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["adm_bc_yes"], callback_data="bc:want:yes")],
        [InlineKeyboardButton(text=t["adm_bc_no"], callback_data="bc:want:no")],
        [InlineKeyboardButton(text=LOCALES[lang]["back"], callback_data="back:admin")]
    ])

def bc_preview_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["adm_bc_send"], callback_data="bc:send")],
        [InlineKeyboardButton(text=t["adm_bc_edit_text"], callback_data="bc:edit:text")],
        [InlineKeyboardButton(text=t["adm_bc_edit_photo"], callback_data="bc:edit:photo")],
        [InlineKeyboardButton(text=t["adm_bc_cancel"], callback_data="bc:cancel")],
    ])