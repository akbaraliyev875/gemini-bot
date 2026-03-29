import logging
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Sizning bot tokeningiz
TOKEN = "8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Sanoq sistemalari bazasi (Kichik harf yoki katta harf farq qilmaydi)
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
    # Har safar /start bosilganda barcha natijalar nollanadi
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
    
    # Natijalarni hisoblash
    correct = data.get('correct', 0)
    total = data.get('total', 0)
    wrong = total - correct

    await message.answer(
        f"🏁 **Sizning natijangiz:**\n\n"
        f"⏱ Umumiy vaqt: {duration} soniya\n"
        f"✅ To'g'ri javoblar: {correct}\n"
        f"❌ Xato javoblar: {wrong}\n"
        f"📊 Jami berilgan savollar: {total}\n\n"
        f"Qayta boshlash uchun /start bosing."
    )
    await state.clear()

@dp.message(QuizState.answering)
async def check_answer(message: types.Message, state: FSMContext):
    # Agar foydalanuvchi komanda yozsa (masalan /stop), javob deb tekshirmaydi
    if message.text.startswith('/'): return

    data = await state.get_data()
    # Foydalanuvchi javobini ham, to'g'ri javobni ham kichik harfga o'tkazib tekshiramiz
    user_answer = message.text.strip().lower()
    correct_answer = data['current_answer'].lower()

    new_total = data['total'] + 1
    new_correct = data['correct']

    if user_answer == correct_answer:
        new_correct += 1
        await message.answer("✅ To'g'ri!")
    else:
        await message.answer(f"❌ Xato! To'g'ri javob: {data['current_answer']}")

    # Ma'lumotlarni yangilaymiz va keyingi savolni beramiz
    await state.update_data(total=new_total, correct=new_correct)
    await ask_question(message, state)

async def main():
    print("Bot terminalda ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
