# ... (tepadagi importlar va start qismlari o'sha-o'sha qoladi)

async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    if data['mode'] == "words":
        question_item = random.choice(WORDS_DATA)
        question = question_item['q']
        answer = str(question_item['a'])
    else:
        # HISOBLASH REJIMI UCHUN GENERATOR (Cheksiz savollar)
        r_type = random.randint(1, 3) # 3 xil turdagi misol
        
        if r_type == 1: # Binary -> Decimal
            num = random.randint(1, 63) # 1 dan 63 gacha sonlar
            question = f"{bin(num)[2:]} (binary) -> o'nlikda?"
            answer = str(num)
        elif r_type == 2: # Decimal -> Binary
            num = random.randint(1, 32)
            question = f"{num} soni binary-da necha bo'ladi?"
            answer = bin(num)[2:]
        else: # Hexadecimal terminlari
            num = random.randint(10, 15)
            hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            question = f"16 likda {num} soni qaysi harf?"
            answer = hex_map[num]

    await state.update_data(current_answer=answer)
    await message.answer(f"❓ {question}")
    await state.set_state(QuizState.answering)
