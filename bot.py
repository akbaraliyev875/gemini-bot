import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Eng chidamli model nomini ishlatamiz
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

INSTRUCTION = (
    "Sen foydalanuvchining yaqin hamrohisan. Samimiy va do'stona gaplash. "
    "Foydalanuvchiga 'akajon' deb murojaat qil. O'zbek tilida javob ber."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi haqiqiy suhbatni boshlasak bo'ladi. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Promptni yuboramiz
        prompt = f"{INSTRUCTION}\n\nFoydalanuvchi: {message.text}"
        
        # Generatsiya qilish
        response = model.generate_content(prompt)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, xabar bo'sh qaytdi. Qaytadan yozib ko'ring-chi?")
            
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        # Xatoni aniq ko'rish uchun (faqat test vaqtida)
        bot.reply_to(message, f"Akajon, nosozlik turi: {str(e)[:50]}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
