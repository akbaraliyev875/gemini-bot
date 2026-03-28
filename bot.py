import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Botning "Aqli"
INSTRUCTION = (
    "Sen foydalanuvchining yaqin hamrohisan. Samimiy, do'stona va o'zbek tilida gaplash. "
    "Foydalanuvchiga 'akajon' deb murojaat qil."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi gaplashsak bo'ladi. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Har bir xabarga AI-dan yangi javob olamiz
        # Hozircha murakkab tarixni chetga surib, oddiy muloqotni yoqamiz
        prompt = f"{INSTRUCTION}\n\nFoydalanuvchi: {message.text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "AI javob qaytara olmadi, qaytadan yozing.")
            
    except Exception as e:
        # Xatoni aniq ko'rish uchun (faqat sizga ko'rinadi)
        error_msg = str(e)
        print(f"Xato yuz berdi: {error_msg}")
        bot.reply_to(message, f"Akajon, ozgina nosozlik: {error_msg[:100]}")

if __name__ == "__main__":
    bot.infinity_polling()
