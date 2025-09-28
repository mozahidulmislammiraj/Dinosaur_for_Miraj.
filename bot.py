# bot.py
import os
import telebot
import requests
import threading
from flask import Flask

# Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # BotFather token
HF_TOKEN = os.getenv("HF_TOKEN")              # Hugging Face token
HF_MODEL = "TheBloke/guanaco-7B-HF"          # Free HF model

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def query_hf(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "options": {"use_cache": False}}
    r = requests.post(f"https://api-inference.huggingface.co/models/{HF_MODEL}",
                      headers=headers, json=payload)
    try:
        return r.json()[0]['generated_text']
    except Exception as e:
        return f"Error: {e}"

@bot.message_handler(func=lambda m: True)
def chat_with_hf(msg):
    reply = query_hf(msg.text)
    bot.reply_to(msg, reply)

# Flask server for Render
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is running ✅"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)