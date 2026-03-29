import logging
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Ma'lumotlar bazasi alohida
WORDS_DATA = [
    {"q": "2 lik sanoq sistemasi (inglizcha)?", "a": "Binary"},
    {"q": "8 lik sanoq sistemasi (inglizcha)?", "a": "Octal"},
    {"q": "10 lik sanoq sistemasi (inglizcha)?", "a": "Decimal"},
    {"q": "16 lik sanoq sistemasi (inglizcha)?", "a": "Hexadecimal"},
]

MATH_DATA = [
    {"q": "1010 (binary) -> o'nlikda?", "a": "10"},
    {"q": "1111 (binary) -> o'nlikda?", "a": "15"},
    {"q": "100 (binary) -> o'nlikda?", "a": "4"},
    {"q": "16 likda 10 soni?", "a": "A"},
    {"q": "16 likda 15 soni?", "a": "F"},
    {"q": "8 likda 7 dan keyingi son?", "a": "10"},
]

class QuizState(StatesGroup):
    choosing_mode = State()
    answering = State()

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 So'zlar")
    builder.button(text="🔢 Hisoblash")
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Rejimni tanlang, akajon:", reply_markup=main_menu())
    await state.set_state(QuizState.choosing_mode)

@dp.message(QuizState.choosing_mode, F.text.in_(["📝 So'zlar", "🔢 Hisoblash"]))
async def set_mode(message: types.Message, state: FSMContext):
    mode = "words" if "So'zlar" in message.text else "math"
    await state.update_data(mode=mode, correct=0, total=0, wrong=0, start_time=time.time())
    await message.answer(f"{message.text} rejimi boshlandi! 🔥\nTo'xtatish uchun /s ni yozing.", reply_markup=types.ReplyKeyboardRemove())
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dataset = WORDS_DATA if data['mode'] == "words" else MATH_DATA
    question_item = random.choice(dataset)
    
    await state.update_data(current_answer=str(question_item['a']))
    await message.answer(f"❓ {question_item['q']}")
    await state.set_state(QuizState.answering)

@dp.message(Command("s")) # Qisqa to'xtatish
async def stop_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'start_time' not in data:
        await message.answer("Avval rejimni tanlang.", reply_markup=main_menu())
        return

    duration = time.time() - data['start_time']
    correct = data.get('correct', 0)
    wrong = data.get('wrong', 0)
    
    wps = round(((correct * 10) / duration) - (wrong * 0.01), 3) if duration > 0 else 0
    final_wps = max(0, wps)

    await message.answer(
        f"🏁 **Natija:**\n\n"
        f"⏱ Vaqt: {round(duration, 1)} sek\n"
        f"✅ To'g'ri: {correct}\n"
        f"❌ Xato: {wrong}\n"
        f"⚡️ **YAKUNIY TEZLIK: {final_wps} WPS**",
        reply_markup=main_menu()
    )
    await state.set_state(QuizState.choosing_mode)

@dp.message(QuizState.answering)
async def check_answer(message: types.Message, state: FSMContext):
    if not message.text or message.text.startswith('/'): return

    data = await state.get_data()
    user_answer = message.text.strip().lower()
    correct_answer = data['current_answer'].lower()
    
    new_correct = data.get('correct', 0)
    new_wrong = data.get('wrong', 0)

    if user_answer == correct_answer:
        new_correct += 1
        await message.answer("✅")
    else:
        new_wrong += 1
        await message.answer(f"❌ To'g'ri javob: {data['current_answer']}\n{data['current_answer']}")

    await state.update_data(correct=new_correct, wrong=new_wrong, total=data.get('total', 0) + 1)
    await ask_question(message, state)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
