import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Xavfsizlik filtrlarini o'chirib qo'yamiz (bot bloklanib qolmasligi uchun)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_history = {}

INSTRUCTION = (
    "Sen foydalanuvchining shaxsiy va eng yaqin hamrohisan. "
    "Foydalanuvchi haqidagi ma'lumotlarni eslab qol. "
    "Samimiy, hazilkash va qadrdon do'stdek gaplash. "
    "Foydalanuvchining uslubiga va shevasiga moslash."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
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
        # Xatoni aniqroq ko'rsatish uchun
        bot.reply_to(message, f"Akajon, ozgina texnik nosozlik: {str(e)[:50]}...")

if __name__ == "__main__":
    bot.infinity_polling()
