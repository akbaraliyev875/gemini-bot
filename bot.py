import logging
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Tokeningiz
TOKEN = "8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

QUIZ_DATA = [
    {"q": "2 lik sanoq sistemasi (inglizcha)?", "a": "Binary"},
    {"q": "8 lik sanoq sistemasi (inglizcha)?", "a": "Octal"},
    {"q": "10 lik sanoq sistemasi (inglizcha)?", "a": "Decimal"},
    {"q": "16 lik sanoq sistemasi (inglizcha)?", "a": "Hexadecimal"},
]

class QuizState(StatesGroup):
    answering = State()

@dp.message(Command("start"))
async def start_quiz(message: types.Message, state: FSMContext):
    await state.clear()
    # correct - to'g'ri, total - jami, wrong - xatolar soni
    await state.update_data(correct=0, total=0, wrong=0, start_time=time.time())
    await message.answer("Quiz boshlandi! 🚀\nHar bir xato uchun -0.01 WPS jarima bor!\nTo'xtatish uchun /stop yozing.")
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    question_item = random.choice(QUIZ_DATA)
    await state.update_data(current_answer=question_item['a'])
    await message.answer(f"❓ {question_item['q']}")
    await state.set_state(QuizState.answering)

@dp.message(Command("stop"))
async def stop_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'start_time' not in data:
        await message.answer("Avval /start ni bosing.")
        return

    duration = time.time() - data['start_time']
    correct = data.get('correct', 0)
    wrong = data.get('wrong', 0)
    total = data.get('total', 0)

    # WPS HISOB-KITOBLARI:
    # 1. Asosiy WPS: (To'g'ri * 10) / vaqt
    base_wps = (correct * 10) / duration if duration > 0 else 0
    
    # 2. Jarima: Har bir xato uchun 0.01
    penalty = wrong * 0.01
    
    # Yakuniy WPS (0 dan pastga tushib ketmasligi uchun max ishlatamiz)
    final_wps = max(0, round(base_wps - penalty, 3))

    await message.answer(
        f"🏁 **Natijangiz:**\n\n"
        f"⏱ Vaqt: {round(duration, 1)} sek\n"
        f"✅ To'g'ri: {correct}\n"
        f"❌ Xato: {wrong}\n"
        f"📊 Jami: {total}\n\n"
        f"⚠️ Jarima: -{round(penalty, 3)} WPS\n"
        f"⚡️ **YAKUNIY TEZLIK: {final_wps} WPS**"
    )
    await state.clear()

@dp.message(QuizState.answering)
async def check_answer(message: types.Message, state: FSMContext):
    if not message.text or message.text.startswith('/'): return

    data = await state.get_data()
    user_answer = message.text.strip().lower()
    correct_answer = data['current_answer']
    
    new_total = data.get('total', 0) + 1
    new_correct = data.get('correct', 0)
    new_wrong = data.get('wrong', 0)

    if user_answer == correct_answer.lower():
        new_correct += 1
        await message.answer("✅")
    else:
        new_wrong += 1
        await message.answer(f"❌ Xato! To'g'ri javob: {correct_answer}\n{correct_answer}")

    await state.update_data(total=new_total, correct=new_correct, wrong=new_wrong)
    await ask_question(message, state)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
