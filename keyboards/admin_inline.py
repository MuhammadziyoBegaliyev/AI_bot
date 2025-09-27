
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales import LOCALES


def admin_root_inline(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    rows = [
        [InlineKeyboardButton(text="📦 Drugs", callback_data="admin:drugs")],
        [InlineKeyboardButton(text="🏥 Pharmacies", callback_data="admin:pharmacies")],
        [InlineKeyboardButton(text="📍 Locations", callback_data="admin:locations")],

        # ✅ Foydalanuvchilar hisobotini Excel/CSV ko'rinishida yuborish
        [InlineKeyboardButton(
            text=t.get("adm_btn_users_export", "📊 Foydalanuvchilar ma’lumoti (Excel)"),
            callback_data="admin:users_export"
        )],

        # 📣 Broadcast (aksiya / xabar) tugmalari
        [
            InlineKeyboardButton(
                text=t.get("adm_btn_send_promo", "📢 Aksiya yuborish"),
                callback_data="adm:promo"
            ),
            InlineKeyboardButton(
                text=t.get("adm_btn_send_msg", "✉️ Habar yuborish"),
                callback_data="adm:msg"
            ),
        ],

        [InlineKeyboardButton(text=t.get("back", "⬅️ Orqaga"), callback_data="back:menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_drugs_inline(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    rows = [
        [InlineKeyboardButton(text="➕ Add drug", callback_data="drug:add")],
        [InlineKeyboardButton(text="📃 List drugs", callback_data="drug:list")],
        [InlineKeyboardButton(text="🗑 Delete drug", callback_data="drug:del")],
        [InlineKeyboardButton(text=t.get("back", "⬅️ Back"), callback_data="admin:root")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_pharm_inline(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    rows = [
        [InlineKeyboardButton(text="➕ Add pharmacy", callback_data="ph:add")],
        [InlineKeyboardButton(text="📃 List pharmacies", callback_data="ph:list")],
        [InlineKeyboardButton(text="🗑 Delete pharmacy", callback_data="ph:del")],
        [InlineKeyboardButton(text=t.get("back", "⬅️ Back"), callback_data="admin:root")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_loc_inline(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    rows = [
        [InlineKeyboardButton(text="➕ Add location", callback_data="loc:add")],
        [InlineKeyboardButton(text="📃 List locations", callback_data="loc:list")],
        [InlineKeyboardButton(text="🗑 Delete location", callback_data="loc:del")],
        [InlineKeyboardButton(text=t.get("back", "⬅️ Back"), callback_data="admin:root")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_pager_inline(kind: str, page: int, has_next: bool) -> InlineKeyboardMarkup:
    # kind in {"drugs","ph","loc"}
    row = []
    if page > 1:
        row.append(InlineKeyboardButton(text="« Prev", callback_data=f"pager:{kind}:{page-1}"))
    if has_next:
        row.append(InlineKeyboardButton(text="Next »", callback_data=f"pager:{kind}:{page+1}"))
    if not row:
        row = [InlineKeyboardButton(text="—", callback_data="noop")]
    return InlineKeyboardMarkup(
        inline_keyboard=[row, [InlineKeyboardButton(text="⬅️ Back", callback_data="admin:root")]]
    )


# --------- Broadcast (promo / message) klaviaturalari ---------

def admin_main_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    rows = [
        [InlineKeyboardButton(text=t.get("adm_btn_send_promo", "📢 Aksiya yuborish"),
                              callback_data="adm:promo")],
        [InlineKeyboardButton(text=t.get("adm_btn_send_msg", "✉️ Habar yuborish"),
                              callback_data="adm:msg")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def bc_yes_no_photo_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t.get("adm_bc_yes", "Ha, rasm qo‘shaman"),
                              callback_data="bc:want:yes")],
        [InlineKeyboardButton(text=t.get("adm_bc_no", "Yo‘q, o‘tkazib yuborish"),
                              callback_data="bc:want:no")],
        [InlineKeyboardButton(text=t.get("back", "⬅️ Orqaga"), callback_data="back:admin")]
    ])


def bc_preview_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES.get(lang, LOCALES["uz"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t.get("adm_bc_send", "📨 Yuborish"), callback_data="bc:send")],
        [InlineKeyboardButton(text=t.get("adm_bc_edit_text", "✏️ Matnni tahrirlash"),
                              callback_data="bc:edit:text")],
        [InlineKeyboardButton(text=t.get("adm_bc_edit_photo", "🖼 Rasmni almashtirish"),
                              callback_data="bc:edit:photo")],
        [InlineKeyboardButton(text=t.get("adm_bc_cancel", "❌ Bekor qilish"),
                              callback_data="bc:cancel")],
    ])
