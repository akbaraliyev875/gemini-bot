import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# DIQQAT: gemini-pro o'rniga gemini-1.5-flash ishlatamiz (bu v1-da aniq bor)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana, 1.5-Flash modeliga o'tdik. Endi ishlashi kerak. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Promptga biroz yo'nalish beramiz
        prompt = f"Sen samimiy o'zbek hamrohisan. Foydalanuvchiga 'akajon' deb murojaat qil. Savol: {message.text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, AI hozircha jim. Qaytadan yozib ko'ring-chi?")
            
    except Exception as e:
        error_str = str(e)
        print(f"Xato: {error_str}")
        # Xatoni aniq ko'rish uchun (masalan: API Key xatosi yoki model xatosi)
        bot.reply_to(message, f"Akajon, muammo chiqdi: {error_str[:100]}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot 1.5-Flash bilan ishga tushdi...")
    bot.infinity_polling()
