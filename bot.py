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

# Savollar bazasi
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
    # Aniq vaqtni (mikrosoniyalargacha) saqlaymiz
    await state.update_data(correct=0, total=0, start_time=time.time())
    await message.answer("Sanoq sistemalari testi boshlandi! 🚀\nTezligingiz (WPS) o'lchanmoqda.\nTo'xtatish uchun /stop ni yozing.")
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
        await message.answer("Siz hali quizni boshlamadinigiz. /start bosing.")
        return

    # To'xtatilgan vaqt
    end_time = time.time()
    duration = end_time - data['start_time']
    
    correct = data.get('correct', 0)
    total = data.get('total', 0)

    # WPS HISOB-KITOBLARI:
    # Formula: To'g'ri javoblar / Ketgan soniya
    # Masalan: 10 ta to'g'ri / 10 soniya = 1.0 WPS
    wps = round(correct / duration, 2) if duration > 0 else 0

    await message.answer(
        f"🏁 **Sizning natijangiz:**\n\n"
        f"⏱ Umumiy vaqt: {round(duration, 1)} soniya\n"
        f"✅ To'g'ri javoblar: {correct}\n"
        f"❌ Xato javoblar: {total - correct}\n"
        f"📊 Jami savollar: {total}\n"
        f"⚡️ **Tezlik (WPS): {wps}**\n\n"
        f"Yana urinib ko'rasizmi? /start"
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

    if user_answer == correct_answer.lower():
        new_correct += 1
        await message.answer("✅ To'g'ri!")
    else:
        # Xatoni to'g'irlash uchun takrorlash
        await message.answer(f"❌ Xato! To'g'ri javob: {correct_answer}")
        await message.answer(f"{correct_answer}")

    await state.update_data(total=new_total, correct=new_correct)
    # Darhol keyingi savol
    await ask_question(message, state)

async def main():
    print("Bot Railway-da ishga tushishga tayyor...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
