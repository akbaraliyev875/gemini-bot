import telebot
import requests
import json

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_gemini_response(user_text):
    # DIQQAT: v1beta emas, barqaror v1 versiyasini ishlatamiz!
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": f"Sen samimiy o'zbek hamrohisan. Foydalanuvchiga 'akajon' deb murojaat qil. Savol: {user_text}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # Agar xato bo'lsa, xato kodini qaytaramiz
            return f"Xato kodi: {response.status_code}. Google javobi: {response.text[:50]}"
    except Exception as e:
        return f"Ulanishda xato: {str(e)[:50]}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi v1 (stable) versiyasiga ulandik. Endi aniq ishlashi kerak! Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = get_gemini_response(message.text)
    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot v1 API bilan ishga tushdi...")
    bot.infinity_polling()
