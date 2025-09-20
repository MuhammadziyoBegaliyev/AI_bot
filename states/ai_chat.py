# path: handlers/ai_chat.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import time

from locales import LOCALES
from utils.lang import get_lang
from filters.registered import RegisteredFilter
from states.ai import AIChat
from keyboards.reply import main_menu
from config import settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

router = Router()

# --- per-user throttling ---
RATE_LIMIT_SECONDS = 5
_last_call_ts: dict[int, float] = {}

def _client_or_none():
    if OpenAI is None:
        return None
    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not api_key:
        return None
    try:
        # retries o'chirilgan – 429 bo'lsa darhol xabar beramiz
        return OpenAI(api_key=api_key, max_retries=0, timeout=30)
    except Exception:
        return None

def _ai_back_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=LOCALES[lang]["back"], callback_data="ai:back")]]
    )

@router.message(RegisteredFilter(), F.text.in_({"🤖 Sun'iy intellekt", "🤖 AI Assistant", "🤖 ИИ-помощник"}))
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    await state.set_state(AIChat.chatting)
    if _client_or_none() is None:
        await message.answer(t["ai_intro"] + "\n\n" + t["ai_no_key"], reply_markup=_ai_back_kb(lang))
    else:
        await message.answer(t["ai_intro"], reply_markup=_ai_back_kb(lang))

@router.message(RegisteredFilter(), AIChat.chatting, F.text)
async def ai_answer(message: Message, state: FSMContext):
    uid = message.from_user.id
    lang = await get_lang(uid)
    t = LOCALES[lang]
    client = _client_or_none()
    if client is None:
        await message.answer(t["ai_no_key"], reply_markup=_ai_back_kb(lang))
        return

    # simple per-user cooldown
    now = time.time()
    if now - _last_call_ts.get(uid, 0) < RATE_LIMIT_SECONDS:
        await message.answer(t["ai_slow_down"], reply_markup=_ai_back_kb(lang))
        return
    _last_call_ts[uid] = now

    user_text = message.text.strip()
    if not user_text:
        await message.answer(t["ai_empty"], reply_markup=_ai_back_kb(lang))
        return

    thinking_msg = await message.answer(t["ai_thinking"], reply_markup=_ai_back_kb(lang))
    system_prompt = t.get("ai_system_prompt", "You are a helpful, concise assistant. Answer in the user's language.")

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
        answer = (resp.choices[0].message.content if resp and resp.choices else None) or t["ai_fail"]
        if len(answer) > 3500:
            answer = answer[:3500] + " …"
        await thinking_msg.edit_text(answer, reply_markup=_ai_back_kb(lang))
    except Exception as e:
        # OpenAI 1.x ko‘pincha APIStatusError beradi; unda status_code bo'ladi
        if getattr(e, "status_code", None) == 429:
            await thinking_msg.edit_text(t["ai_rate_limited"], reply_markup=_ai_back_kb(lang))
        else:
            await thinking_msg.edit_text(t["ai_fail"], reply_markup=_ai_back_kb(lang))

@router.message(RegisteredFilter(), AIChat.chatting, ~F.text)  # matn bo'lmagan hamma narsaga
async def ai_non_text(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_text_only"], reply_markup=_ai_back_kb(lang))

@router.callback_query(F.data == "ai:back")
async def ai_back(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_lang(cb.from_user.id)
    await cb.message.edit_text(LOCALES[lang]["ai_ended"])
    await cb.message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))
    await cb.answer()
