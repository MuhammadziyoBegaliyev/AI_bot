# path: handlers/ai_chat.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from utils.lang import get_lang
from filters.registered import RegisteredFilter
from states.ai import AIChat
from keyboards.reply import main_menu

# OpenAI mijozini xavfsiz import
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from config import settings

router = Router()


def _client_or_none():
    """OpenAI klientini qaytaradi yoki None (kalit/mijoz bo'lmasa)."""
    if OpenAI is None:
        return None
    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def _ai_back_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=LOCALES[lang]["back"], callback_data="ai:back")]
        ]
    )


# 1) Asosiy menyudan AI chatga kirish
@router.message(
    RegisteredFilter(),
    F.text.in_({"🤖 Sun'iy intellekt", "🤖 AI Assistant", "🤖 ИИ-помощник"})
)
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]

    await state.set_state(AIChat.chatting)

    # Kalit bo‘lmasa ham foydalanuvchi uchun neytral xabar
    if _client_or_none() is None:
        await message.answer(
            t["ai_intro"] + "\n\n" + t["ai_no_key"],
            reply_markup=_ai_back_kb(lang),
        )
    else:
        await message.answer(t["ai_intro"], reply_markup=_ai_back_kb(lang))


# 2) AI chat: istalgan matnga javob
@router.message(RegisteredFilter(), AIChat.chatting, F.text)
async def ai_answer(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    client = _client_or_none()

    if client is None:
        await message.answer(t["ai_no_key"], reply_markup=_ai_back_kb(lang))
        return

    user_text = message.text.strip()
    if not user_text:
        await message.answer(t["ai_empty"], reply_markup=_ai_back_kb(lang))
        return

    # “Yozayapman…” xabarini yuborib turamiz
    thinking_msg = await message.answer(t["ai_thinking"], reply_markup=_ai_back_kb(lang))

    system_prompt = t.get(
        "ai_system_prompt",
        "You are a helpful, concise assistant. Answer in the user's language."
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_text},
            ],
            temperature=0.6,
            max_tokens=600,
        )
        answer = resp.choices[0].message.content if resp and resp.choices else t["ai_fail"]
        if answer and len(answer) > 3500:
            answer = answer[:3500] + " …"
        await thinking_msg.edit_text(answer, reply_markup=_ai_back_kb(lang))
    except Exception:
        await thinking_msg.edit_text(t["ai_fail"], reply_markup=_ai_back_kb(lang))


# 3) Rasm yuborilsa – hozircha qo‘llanmaydi
@router.message(RegisteredFilter(), AIChat.chatting, F.photo)
async def ai_photo_stub(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_no_image"], reply_markup=_ai_back_kb(lang))


# 4) Inline “⬅️ Orqaga”
@router.callback_query(F.data == "ai:back")
async def ai_back(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_lang(cb.from_user.id)
    await cb.message.edit_text(LOCALES[lang]["ai_ended"])
    await cb.message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))
    await cb.answer()
