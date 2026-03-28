import telebot
import google.generativeai as genai

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# MODELNI TANLASH: Agar 1.5-flash xato bersa, eng sodda 'gemini-1.5-flash-latest'ni sinaymiz
# Bu SDK-ga eng yangi va mos keladigan modelni tanlashga yordam beradi
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana, modelni yangiladik. Endi ishlashi shart! Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk_with_gemini(message):
    try:
        # Promptni yuboramiz
        response = model.generate_content(f"Sen samimiy o'zbek hamrohisan. Savol: {message.text}")
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Akajon, AI hozircha jim. Qaytadan yozing-chi?")
            
    except Exception as e:
        error_msg = str(e)
        print(f"Xato: {error_msg}")
        # Agar yana 404 bersa, demak kutubxona yangilanmagan
        bot.reply_to(message, f"Akajon, nosozlik: {error_msg[:100]}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot 1.5-Flash-Latest bilan ishga tushdi...")
    bot.infinity_polling()
