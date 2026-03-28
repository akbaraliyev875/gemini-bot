import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Modelni o'zgartirdik: gemini-pro (bu 404 xatosini bermaydi)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_history = {}

INSTRUCTION = (
    "Sen foydalanuvchining shaxsiy va eng yaqin hamrohisan. "
    "Foydalanuvchi haqidagi ma'lumotlarni eslab qol. "
    "Samimiy, hazilkash va qadrdon do'stdek gaplash. "
    "Foydalanuvchining uslubiga va shevasiga moslash. "
    "Javoblaring qisqa va qiziqarli bo'lsin."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    # Har safar /start bosilganda yangi toza suhbat boshlanadi
    chat_history[chat_id] = model.start_chat(history=[])
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi haqiqiy suhbatni boshlasak bo'ladi. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    chat_id = message.chat.id
    
    if chat_id not in chat_history:
        chat_history[chat_id] = model.start_chat(history=[])
    
    try:
        # Chat tarixiga tayanib javob berish
        full_prompt = f"{INSTRUCTION}\n\nFoydalanuvchi: {message.text}"
        
        response = chat_history[chat_id].send_message(full_prompt)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Xato: {e}")
        bot.reply_to(message, "Akajon, ozgina miyam charchadi. Qaytadan yozing-chi?")

if __name__ == "__main__":
    bot.infinity_polling()
