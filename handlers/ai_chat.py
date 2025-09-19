
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from locales import LOCALES
from utils.lang import get_lang
from keyboards.reply import ai_chat_kb, main_menu
from filters.registered import RegisteredFilter

from dataclasses import dataclass
from typing import List, Dict

from openai import OpenAI
from config import settings

router = Router()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# FSM holati
from aiogram.fsm.state import StatesGroup, State
class AIChat(StatesGroup):
    waiting = State()

# 1) Asosiy menyudan AI tugmasi bosilganda
@router.message(RegisteredFilter(), F.text.in_({"🤖 Sun'iy intellekt", "🤖 AI Assistant", "🤖 ИИ-помощник"}))
async def ai_enter(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(AIChat.waiting)
    # Tarixni boshlab qo'yamiz (engil kontekst uchun 10 xabar saqlaymiz)
    await state.update_data(history=[])
    await message.answer(LOCALES[lang]["ai_intro"], reply_markup=ai_chat_kb(lang))

# 2) Orqaga bosilsa — chiqish
@router.message(RegisteredFilter(), AIChat.waiting, F.text.func(lambda s: s and s.strip() in {"⬅️ Orqaga","⬅️ Back","⬅️ Назад"}))
async def ai_exit(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.clear()
    await message.answer(LOCALES[lang]["ai_ended"], reply_markup=main_menu(lang))

# 3) Foydalanuvchi savoli — ChatGPT’dan javob qaytarish
@router.message(RegisteredFilter(), AIChat.waiting, F.text)
async def ai_ask(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    data = await state.get_data()
    history: List[Dict[str, str]] = data.get("history", [])

    user_text = message.text.strip()

    # Kichik sistem prompt (tilga mos)
    sys_prompts = {
        "uz": "Siz foydalanuvchiga o‘zbek tilida aniq va qisqa javob beruvchi yordamchisiz.",
        "en": "You are a helpful assistant. Answer in concise, clear English.",
        "ru": "Вы полезный ассистент. Отвечайте кратко и ясно на русском.",
    }
    system_msg = {"role": "system", "content": sys_prompts.get(lang, sys_prompts["uz"])}

    # Tarixni yig‘amiz (oxirgi 10 ta xabar)
    messages = [system_msg] + history + [{"role": "user", "content": user_text}]

    # Tip berish
    await message.answer(LOCALES[lang]["ai_thinking"])

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=600,
        )
        answer = resp.choices[0].message.content.strip() if resp.choices else "…"
    except Exception as e:
        answer = {
            "uz": "Kechirasiz, hozir javob bera olmadim.",
            "en": "Sorry, I couldn’t answer right now.",
            "ru": "Извините, сейчас не удалось ответить.",
        }.get(lang, "Kechirasiz, hozir javob bera olmadim.")

    # Yangi tarixni saqlaymiz
    history = (history + [{"role": "user", "content": user_text}, {"role": "assistant", "content": answer}])[-10:]
    await state.update_data(history=history)

    await message.answer(answer, reply_markup=ai_chat_kb(lang))
