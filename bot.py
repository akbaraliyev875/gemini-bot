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

# /start ham, /p ham ishlayveradi
@dp.message(Command("start", "p"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Tayyormisiz? Rejimni tanlang:\n\n"
        "📝 **So'zlar** - Terminlar\n"
        "🔢 **Hisoblash** - Cheksiz misollar", 
        reply_markup=main_menu()
    )
    await state.set_state(QuizState.choosing_mode)

@dp.message(QuizState.choosing_mode, F.text.in_(["📝 So'zlar", "🔢 Hisoblash"]))
async def set_mode(message: types.Message, state: FSMContext):
    mode = "words" if "So'zlar" in message.text else "math"
    await state.update_data(mode=mode, correct=0, total=0, wrong=0, start_time=time.time())
    await message.answer(
        f"{message.text} rejimi boshlandi! 🚀\n"
        f"To'xtatish uchun: /s", 
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['mode'] == "words":
        item = random.choice(WORDS_DATA)
        question, answer = item['q'], item['a']
    else:
        r_type = random.randint(1, 3)
        if r_type == 1:
            num = random.randint(1, 31)
            question, answer = f"{bin(num)[2:]} (binary) -> o'nlikda?", str(num)
        elif r_type == 2:
            num = random.randint(1, 20)
            question, answer = f"{num} soni binary-da necha?", bin(num)[2:]
        else:
            num = random.randint(10, 15)
            hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            question, answer = f"16 likda {num} soni qaysi harf?", hex_map[num]

    await state.update_data(current_answer=answer)
    await message.answer(f"❓ {question}")
    await state.set_state(QuizState.answering)

@dp.message(Command("s"))
async def stop_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'start_time' not in data:
        await message.answer("O'yin boshlanmagan. Boshlash uchun /p ni bosing.", reply_markup=main_menu())
        return

    duration = time.time() - data['start_time']
    correct, wrong = data.get('correct', 0), data.get('wrong', 0)
    base_wps = (correct * 10) / duration if duration > 0 else 0
    final_wps = max(0, round(base_wps - (wrong * 0.01), 3))

    await message.answer(
        f"🏁 **Natijangiz:**\n\n⏱ Vaqt: {round(duration, 1)} sek\n✅ To'g'ri: {correct}\n❌ Xato: {wrong}\n⚡️ **YAKUNIY: {final_wps} WPS**",
        reply_markup=main_menu()
    )
    await state.set_state(QuizState.choosing_mode)

@dp.message(QuizState.answering)
async def check_answer(message: types.Message, state: FSMContext):
    if not message.text or message.text.startswith('/'): return
    data = await state.get_data()
    if message.text.strip().lower() == data['current_answer'].lower():
        await state.update_data(correct=data.get('correct', 0) + 1)
        await message.answer("✅")
    else:
        await state.update_data(wrong=data.get('wrong', 0) + 1)
        await message.answer(f"❌ To'g'ri: {data['current_answer']}\n{data['current_answer']}")
    await ask_question(message, state)

async def main():
    # FAQAT /p VA /s MENYUGA CHIQADI
    commands = [
        types.BotCommand(command="p", description="O'yinni boshlash / Play"),
        types.BotCommand(command="s", description="To'xtatish va natija / Stop")
    ]
    await bot.set_my_commands(commands)
    
    print("Bot tayyor...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
