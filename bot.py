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

# Tokeningiz
TOKEN = "8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# So'zlar bazasi (Terminologiya uchun)
WORDS_DATA = [
    {"q": "2 lik sanoq sistemasi (inglizcha)?", "a": "Binary"},
    {"q": "8 lik sanoq sistemasi (inglizcha)?", "a": "Octal"},
    {"q": "10 lik sanoq sistemasi (inglizcha)?", "a": "Decimal"},
    {"q": "16 lik sanoq sistemasi (inglizcha)?", "a": "Hexadecimal"},
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
    await message.answer(
        "Xush kelibsiz, akajon! Rejimni tanlang:\n\n"
        "📝 **So'zlar** - Terminlarni tez yozish\n"
        "🔢 **Hisoblash** - Cheksiz matematik misollar", 
        reply_markup=main_menu()
    )
    await state.set_state(QuizState.choosing_mode)

@dp.message(QuizState.choosing_mode, F.text.in_(["📝 So'zlar", "🔢 Hisoblash"]))
async def set_mode(message: types.Message, state: FSMContext):
    mode = "words" if "So'zlar" in message.text else "math"
    await state.update_data(mode=mode, correct=0, total=0, wrong=0, start_time=time.time())
    await message.answer(
        f"{message.text} rejimi boshlandi! 🚀\n"
        f"To'xtatish uchun: /s\n"
        f"Har bir xato uchun: -0.01 WPS", 
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    if data['mode'] == "words":
        # So'zlar rejimida ro'yxatdan tasodifiy tanlash
        item = random.choice(WORDS_DATA)
        question = item['q']
        answer = item['a']
    else:
        # HISOBLASH GENERATORI (Cheksiz va har xil)
        r_type = random.randint(1, 3)
        if r_type == 1: # Binary to Decimal
            num = random.randint(1, 31) # 5-bitgacha (tezlik uchun)
            question = f"{bin(num)[2:]} (binary) -> o'nlikda?"
            answer = str(num)
        elif r_type == 2: # Decimal to Binary
            num = random.randint(1, 20)
            question = f"{num} soni binary-da necha bo'ladi?"
            answer = bin(num)[2:]
        else: # Hex Hex symbols
            num = random.randint(10, 15)
            hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            question = f"16 likda {num} soni qaysi harf?"
            answer = hex_map[num]

    await state.update_data(current_answer=answer)
    await message.answer(f"❓ {question}")
    await state.set_state(QuizState.answering)

@dp.message(Command("s")) # Qisqa to'xtatish buyrug'i
async def stop_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'start_time' not in data:
        await message.answer("Avval rejimni tanlang.", reply_markup=main_menu())
        return

    duration = time.time() - data['start_time']
    correct = data.get('correct', 0)
    wrong = data.get('wrong', 0)
    
    # WPS Formula: (To'g'ri * 10 / vaqt) - (xatolar * 0.01)
    base_wps = (correct * 10) / duration if duration > 0 else 0
    penalty = wrong * 0.01
    final_wps = max(0, round(base_wps - penalty, 3))

    await message.answer(
        f"🏁 **Natijangiz:**\n\n"
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
    print("Bot muvaffaqiyatli ishga tushdi...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
