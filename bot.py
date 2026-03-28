import telebot
import requests
import json

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_gemini_response(user_text):
    # DIQQAT: Bu eng barqaror va xatosiz URL manzil!
    # v1 versiyasi va models/gemini-1.5-flash to'liq nomi
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Sen samimiy o'zbek hamrohisan. Foydalanuvchiga 'akajon' deb murojaat qil. Savol: {user_text}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Akajon, AI hozircha javob bermadi. Qaytadan yozing."
        else:
            # Agar v1 ham 404 bersa, demak API KEY'da mintaqa cheklovi bor
            return f"Xato kodi: {response.status_code}. Google javobi: {response.text[:100]}..."
            
    except Exception as e:
        return f"Ulanish xatosi: {str(e)[:50]}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊  Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        ai_response = get_gemini_response(message.text)
        bot.reply_to(message, ai_response)
    except Exception:
        bot.reply_to(message, "Akajon, nosozlik yuz berdi. Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot v1 Stable bilan ishga tushdi...")
    bot.infinity_polling()
