import logging
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Tokeningiz o'z joyida
TOKEN = "8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Sanoq sistemalari bazasi
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
    await state.update_data(correct=0, total=0, start_time=time.time())
    await message.answer("Sanoq sistemalari testi boshlandi! 🚀\nTo'xtatish uchun /stop ni yozing.")
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
        await message.answer("Siz hali quizni boshlamadingiz. /start ni bosing.")
        return

    end_time = time.time()
    duration = int(end_time - data['start_time'])
    
    correct = data.get('correct', 0)
    total = data.get('total', 0)

    await message.answer(
        f"🏁 **Natijangiz:**\n\n"
        f"⏱ Vaqt: {duration} soniya\n"
        f"✅ To'g'ri: {correct}\n"
        f"❌ Xato: {total - correct}\n"
        f"📊 Jami: {total}"
    )
    await state.clear()

@dp.message(QuizState.answering)
async def check_answer(message: types.Message, state: FSMContext):
    if message.text.startswith('/'): return

    data = await state.get_data()
    user_answer = message.text.strip().lower()
    correct_answer = data['current_answer'] # Asl holati (masalan Binary)
    
    new_total = data['total'] + 1
    new_correct = data['correct']

    if user_answer == correct_answer.lower():
        new_correct += 1
        await message.answer("✅ To'g'ri!")
    else:
        # Xato bo'lganda to'g'ri javobni takrorlab yuboradi
        await message.answer(f"❌ Xato!\nTo'g'ri javob: {correct_answer}")
        await message.answer(f"{correct_answer}") # Mana bu joyda takrorlaydi

    await state.update_data(total=new_total, correct=new_correct)
    # Keyingi random savolga o'tish
    await ask_question(message, state)

async def main():
    print("Bot terminalda ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
