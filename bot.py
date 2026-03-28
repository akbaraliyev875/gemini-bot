import telebot
import requests
import json

# Ma'lumotlar
TELEGRAM_TOKEN = '8619873269:AAF7Iy4PfmLzLdgf34ZtFHBjrHuqs1nNOYU'
GEMINI_API_KEY = 'AIzaSyDDxc3tGcgosIUXm30i35f94hd_Knmp2kE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_gemini_response(user_text):
    # DIQQAT: Eng chidamli v1beta va gemini-pro modeli
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
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
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Akajon, AI javob bera olmadi. Qaytadan yozing-chi?"
        else:
            # Xato chiqsa, model nomini o'zgartirib ko'ramiz
            return f"Xato kodi: {response.status_code}. Google: {response.text[:80]}..."
            
    except Exception as e:
        return f"Ulanishda xato: {str(e)[:50]}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum, akajon! 😊 Mana, eng barqaror Gemini-Pro modeliga o'tdik. Endi ishlashi kerak! Nima gaplar?")

@bot.message_handler(func=lambda message: True)
def talk(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        ai_response = get_gemini_response(message.text)
        bot.reply_to(message, ai_response)
    except Exception:
        bot.reply_to(message, "Akajon, ozgina texnik nosozlik bo'ldi.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot Gemini-Pro bilan ishga tushdi...")
    bot.infinity_polling()
    
