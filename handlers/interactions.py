from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.search import SearchFlow
from utils.lang import get_lang
from locales import LOCALES

router = Router()

def check_interaction(names: list[str]) -> str | None:
    s = {n.lower() for n in names}
    if "ibuprofen" in s and "aspirin" in s:
        return "Ibuprofen + Aspirin: qon ketish xavfi oshishi mumkin."
    return None

@router.message(F.text.regexp(r"^interact\b|^o'zaro|^взаимод"))
async def start_interactions(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(SearchFlow.interactions)
    await state.update_data(drugs=[])
    txt = {
        "uz": "Dorilarni birma-bir yuboring. Tugatgach /done yozing.",
        "en": "Send drug names one by one. Type /done when finished.",
        "ru": "Отправляйте названия препаратов по одному. В конце введите /done.",
    }.get(lang, "Send drug names and type /done when finished.")
    await message.answer(txt)

@router.message(SearchFlow.interactions, F.text)
async def add_drug(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    data = await state.get_data()
    arr = data.get("drugs", [])
    if message.text.strip().lower() == "/done":
        if len(arr) >= 2:
            warn = check_interaction(arr)
            if warn:
                await message.answer(("⚠️ " if lang != "ru" else "⚠️ ") + warn)
            else:
                ok = {"uz": "✅ Xavfli kombinatsiya topilmadi.",
                      "en": "✅ No dangerous interaction found.",
                      "ru": "✅ Опасных взаимодействий не обнаружено."}.get(lang)
                await message.answer(ok)
        else:
            need2 = {"uz": "Kamida 2 ta dori kiriting.",
                     "en": "Enter at least two drugs.",
                     "ru": "Введите минимум два препарата."}.get(lang)
            await message.answer(need2)
        await state.clear()
        return

    arr.append(message.text.strip())
    await state.update_data(drugs=arr)
    prompt = {
        "uz": "Yana dori nomini kiriting yoki /done yozing.",
        "en": "Enter another drug name or type /done.",
        "ru": "Введите ещё один препарат или напишите /done.",
    }.get(lang)
    await message.answer(prompt)
