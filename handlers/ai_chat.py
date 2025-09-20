# path: handlers/ai_chat.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from utils.lang import get_lang
from filters.registered import RegisteredFilter
from states.ai import AIChat
from config import settings

try:
    from openai import OpenAI, RateLimitError
except Exception:
    OpenAI = None
    RateLimitError = Exception

router = Router()

def _ai_back_kb(lang: str) -> InlineKeyboardMarkup:
    t = LOCALES[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["back"], callback_data="back:menu")]
    ])

def _client():
    if OpenAI is None:
        return None
    key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not key:
        return None
    try:
        return OpenAI(api_key=key)
    except Exception:
        return None

@router.message(
    RegisteredFilter(),
    F.text.in_({"🤖 Sun'iy intellekt", "🤖 AI Assistant", "🤖 ИИ-помощник"})
)
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    await state.set_state(AIChat.chatting)

    if _client() is None:
        await message.answer(t["ai_no_key"], reply_markup=_ai_back_kb(lang))
    else:
        await message.answer(t["ai_welcome"], reply_markup=_ai_back_kb(lang))

@router.message(RegisteredFilter(), AIChat.chatting, F.text)
async def ai_answer(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    t = LOCALES[lang]
    client = _client()

    if client is None:
        await message.answer(t["ai_no_key"], reply_markup=_ai_back_kb(lang))
        return

    user_text = message.text.strip()
    if not user_text:
        await message.answer(t["ai_empty"], reply_markup=_ai_back_kb(lang))
        return

    thinking = await message.answer(t["ai_thinking"], reply_markup=_ai_back_kb(lang))
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": t["ai_system_prompt"]},
                {"role": "user", "content": user_text}
            ],
            temperature=0.4,
            max_tokens=256,
        )
        answer = (resp.choices[0].message.content or "").strip()
        if not answer:
            answer = t["ai_fail"]
        await thinking.edit_text(answer, reply_markup=_ai_back_kb(lang))
    except RateLimitError:
        await thinking.edit_text(t["ai_rate_limited"], reply_markup=_ai_back_kb(lang))
    except Exception:
        await thinking.edit_text(t["ai_fail"], reply_markup=_ai_back_kb(lang))

@router.message(RegisteredFilter(), AIChat.chatting, F.photo)
async def ai_photo_stub(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(LOCALES[lang]["ai_no_image"])

# “back:menu” inline tugmasi uchun umumiy handler (sizda allaqachon bor bo‘lsa, shu qismni takrorlamang)
from aiogram.types import CallbackQuery
from keyboards.reply import main_menu

@router.callback_query(F.data == "back:menu")
async def inline_back_to_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = await get_lang(cb.from_user.id)
    await cb.message.edit_text(LOCALES[lang]["menu"])
    await cb.message.answer(LOCALES[lang]["menu"], reply_markup=main_menu(lang))
    await cb.answer()
