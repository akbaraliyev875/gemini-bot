import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# DIQQAT: Modelni to'liq nomi bilan chaqiramiz (models/ qo'shimchasi bilan)
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi to'liq yo'l bilan ulandik. Ishlashi kerak! Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Promptni yuboramiz
        prompt = f"Sen samimiy o'zbek hamrohisan. Foydalanuvchiga 'akajon' deb murojaat qil. Savol: {message.text}"
        
        # Javobni olish
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, javob bo'sh qaytdi. Qaytadan urinib ko'ring-chi?")
            
    except Exception as e:
        error_msg = str(e)
        print(f"Xato: {error_msg}")
        # Xatoni aniq ko'rish uchun (faqat boshlanishini chiqaramiz)
        bot.reply_to(message, f"Akajon, nosozlik: {error_msg[:80]}...")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot models/gemini-1.5-flash bilan ishga tushdi...")
    bot.infinity_polling()
