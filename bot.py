import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Modelni eng yangi versiyasiga o'zgartirdik
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Botning "xarakteri"
INSTRUCTION = (
    "Sen foydalanuvchining shaxsiy va eng yaqin hamrohisan. "
    "Muloqotda samimiy bo'l, foydalanuvchiga 'akajon' deb murojaat qil. "
    "Foydalanuvchi haqidagi ma'lumotlarni eslab qol va unga moslash. "
    "O'zbek tilida, kerak bo'lsa samimiy shevada gaplash."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi hammasi joyida. "
                          "Yangi hamrohingiz gaplashishga tayyor. Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Oddiy va aniq muloqot usuli
        prompt = f"{INSTRUCTION}\n\nFoydalanuvchi: {message.text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, tushunarsiz javob bo'ldi, qaytadan yozing-chi?")
            
    except Exception as e:
        print(f"Xato: {e}")
        # Xatoni logga chiqaramiz va foydalanuvchiga xabar beramiz
        bot.reply_to(message, f"Akajon, ozgina texnik nosozlik bo'ldi. Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    # Avvalgi webhook-larni tozalaymiz
    bot.remove_webhook()
    print("Gemini-1.5-flash bot ishga tushdi...")
    bot.infinity_polling()
