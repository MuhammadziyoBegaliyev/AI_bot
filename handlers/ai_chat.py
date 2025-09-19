# path: handlers/ai_chat.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from utils.lang import get_lang
from filters.registered import RegisteredFilter

from states.ai_chat import AIChat
from config import settings

# OpenAI mijozini xavfsiz import + mavjud bo'lmasa graceful degrade
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

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

# 1) Asosiy menyudan AI chatga kirish
@router.message(
    RegisteredFilter(),
    F.text.in_({"🤖 Sun’iy intellekt", "🤖 AI Assistant", "🤖 ИИ ассистент"})
)
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(AIChat.chatting)
    t = LOCALES[lang]
    # Kalit bor-yo'qligini userga ko'rsatmay, muloyim ogohlantiramiz
    if _client_or_none() is None:
        await message.answer(
            t["ai_welcome"]
            + "\n\n"
            + t["ai_no_key"]  # foydalanuvchi uchun neytral xabar
        )
    else:
        await message.answer(t["ai_welcome"])

# 2) AI chat: istalgan matnga javob
@router.message(RegisteredFilter(), AIChat.chatting, F.text)
async def ai_answer(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    client = _client_or_none()
    if client is None:
        # Admin uchun ko‘proq diagnostika (faqat GROUP_ID/Admin bo’lsa yaxshi, lekin hozir soddaroq)
        await message.answer(t["ai_no_key"])
        return

    user_text = message.text.strip()
    if not user_text:
        await message.answer(t["ai_empty"])
        return

    # System prompt — tilga mos
    system_prompt = t["ai_system_prompt"]

    try:
        # Chat Completions (OpenAI Python SDK >=1.0)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_text}
            ],
            temperature=0.6,
            max_tokens=600,
        )
        answer = resp.choices[0].message.content if resp and resp.choices else t["ai_fail"]
        # Xavfsizlik: juda uzun bo'lsa bir oz kesamiz
        if answer and len(answer) > 3500:
            answer = answer[:3500] + " …"
        await message.answer(answer or t["ai_fail"])
    except Exception:
        await message.answer(t["ai_fail"])

# 3) Rasm yuborilsa (hozircha qo‘llab-quvvatlanmagan)
@router.message(RegisteredFilter(), AIChat.chatting, F.photo)
async def ai_photo_stub(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_no_image"])

# 4) /ai_stop yoki “menu” ga qaytish
@router.message(RegisteredFilter(), AIChat.chatting, F.text.func(lambda s: s and s.lower() in {"/ai_stop", "stop"}))
async def ai_stop(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_stopped"])
