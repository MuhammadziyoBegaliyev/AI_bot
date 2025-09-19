# path: handlers/ai_chat.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from utils.lang import get_lang
from filters.registered import RegisteredFilter
from states.ai import AIChat          # ← correct import
from config import settings

# OpenAI client (optional)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

router = Router()

def _client_or_none():
    if OpenAI is None:
        return None
    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def _norm(s: str) -> str:
    if not s:
        return ""
    # remove emoji and normalize apostrophes/spaces
    s = s.replace("🤖", "").replace("’", "'").strip().lower()
    return s

TRIGGERS = {
    "sun'iy intellekt",      # UZ
    "ai assistant",          # EN
    "ии ассистент",          # RU
    "ai chat",               # fallback
}

# 1) Enter AI chat from main menu or via /ai
@router.message(
    RegisteredFilter(),
    F.text.func(lambda t: t and (_norm(t) in TRIGGERS)) | F.text.regexp(r"^/ai\b", flags=0)
)
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    await state.set_state(AIChat.chatting)
    if _client_or_none() is None:
        await message.answer(t["ai_welcome"] + "\n\n" + t["ai_no_key"])
    else:
        await message.answer(t["ai_welcome"])

# 2) Chat loop
@router.message(RegisteredFilter(), AIChat.chatting, F.text)
async def ai_answer(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]

    # Exit?
    txt_norm = _norm(message.text)
    if txt_norm in { "back", "orqaga", "назад" } or message.text.strip().lower() in {"/ai_stop", "stop"}:
        await state.clear()
        await message.answer(t["ai_stopped"])
        return

    client = _client_or_none()
    if client is None:
        await message.answer(t["ai_no_key"])
        return

    user_text = message.text.strip()
    if not user_text:
        await message.answer(t["ai_empty"])
        return

    system_prompt = t["ai_system_prompt"]

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.6,
            max_tokens=600,
        )
        answer = (resp.choices[0].message.content or "").strip() if resp and resp.choices else ""
        if not answer:
            answer = t["ai_fail"]
        if len(answer) > 3500:
            answer = answer[:3500] + " …"
        await message.answer(answer)
    except Exception:
        await message.answer(t["ai_fail"])

# 3) Photo stub (optional)
@router.message(RegisteredFilter(), AIChat.chatting, F.photo)
async def ai_photo_stub(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_no_image"])
