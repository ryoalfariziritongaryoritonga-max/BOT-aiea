  import os
import threading
from flask import Flask
import telebot
from google import genai

# 1. Server Dummy Web untuk Render Web Service
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot AIEA is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Kode Bot Telegram & Gemini
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_pesan = message.text
    print(f"Pesan masuk: {user_pesan}")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Kamu adalah AI Executive Assistant yang ramah dan siap membantu. Jawablah pesan ini: {user_pesan}",
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Maaf, terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Jalankan server web di thread terpisah
    threading.Thread(target=run_web_server).start()
    
    # Jalankan bot Telegram
    print("Bot sedang berjalan...")
    bot.infinity_polling()
