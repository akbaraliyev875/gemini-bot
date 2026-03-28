import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni eng sodda usulda sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi hammasi joyida. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Eng sodda va eng chidamli muloqot
        response = model.generate_content(f"Siz samimiy do'stsiz. Foydalanuvchiga 'akajon' deb murojaat qiling. Savol: {message.text}")
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, Google hozircha javob bermadi, qaytadan yozing.")
            
    except Exception as e:
        # Xatoni logda ko'rish uchun
        print(f"Xato: {e}")
        bot.reply_to(message, f"Akajon, texnik nosozlik: {str(e)[:50]}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
