import telebot
import requests
import json

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_gemini_response(user_text):
    # Google API-ning eng aniq va ishlaydigan nuqtasi
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    # So'rov strukturasi (Google talab qilganidek to'liq shaklda)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Sen foydalanuvchining yaqin hamrohisan. Samimiy va do'stona gaplash. Foydalanuvchiga 'akajon' deb murojaat qil. O'zbek tilida javob ber. Savol: {user_text}"}
                ]
            }
        ]
    }
    
    try:
        # Request yuboramiz
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            # Javobni xavfsiz olish
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Akajon, AI hozircha javob bera olmadi. Qaytadan yozing-chi?"
        else:
            # Xato kodi va xabarni aniq ko'ramiz
            return f"Xato kodi: {response.status_code}. Google xabari: {response.text[:100]}..."
            
    except Exception as e:
        return f"Ulanishda xato: {str(e)[:50]}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana endi hammasi cho'tka bo'ldi. Gaplashamizmi?")

@bot.message_handler(func=lambda message: True)
def talk(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        ai_response = get_gemini_response(message.text)
        bot.reply_to(message, ai_response)
    except Exception:
        bot.reply_to(message, "Akajon, ozgina texnik nosozlik bo'ldi. Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot yangilangan API bilan ishga tushdi...")
    bot.infinity_polling()
