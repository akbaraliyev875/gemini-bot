import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Filtrlarni o'chirish (Xatolik bermasligi uchun)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Model nomi: eng oddiy va barqaror shaklda
model = genai.GenerativeModel(model_name='gemini-1.5-flash', safety_settings=safety_settings)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi hammasi cho'tka bo'ldi. Gaplashamizmi?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Eng sodda muloqot: Instruction-siz tekshiramiz
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, javob bo'sh qaytdi. Qaytadan yozing-chi?")
            
    except Exception as e:
        print(f"Xato: {e}")
        # Xatoni aniq ko'rsatish
        bot.reply_to(message, f"Akajon, nosozlik turi: {str(e)[:60]}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot ishga tushdi...")
    bot.infinity_polling()
