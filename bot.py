import telebot
import google.generativeai as genai

# Ma'lumotlar (Yangi Tokenlar)
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Suhbat tarixini saqlash uchun lug'at
chat_history = {}

# Botning xarakteri (Siz aytgan hamrohlik buyrug'i)
INSTRUCTION = (
    "Sen foydalanuvchining shaxsiy va eng yaqin hamrohisan. "
    "Sening vazifang - foydalanuvchi haqidagi ma'lumotlarni eslab qolish "
    "va uning gapirish uslubiga, shevasiga moslashish. "
    "Suhbat davomida foydalanuvchini o'rgan va unga samimiy do'stdek (masalan, akajon deb) murojaat qil. "
    "Rasmiy botdek emas, tirik insondek, hazil-huzul bilan gaplash."
)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    chat_history[chat_id] = model.start_chat(history=[])
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Yangi hamrohingiz tayyor. Nima gaplar? Kayfiyatlar qalay?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    chat_id = message.chat.id
    
    if chat_id not in chat_history:
        chat_history[chat_id] = model.start_chat(history=[])
    
    try:
        # Har safar yo'riqnomani eslatib turamiz
        full_prompt = f"[Eslatma: {INSTRUCTION}]\n\nUser: {message.text}"
        
        response = chat_history[chat_id].send_message(full_prompt)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Xato: {e}")
        bot.reply_to(message, "Akajon, ozgina miyam charchadi. Qaytadan yozing-chi?")

if __name__ == "__main__":
    bot.infinity_polling()
