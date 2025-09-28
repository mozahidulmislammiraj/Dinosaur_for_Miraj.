import os, telebot, requests
from flask import Flask
import threading

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
HF_MODEL = "EleutherAI/gpt-neo-2.7B"  # lightweight model

def query_hf(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    json_data = {"inputs": prompt}
    r = requests.post(f"https://api-inference.huggingface.co/models/{HF_MODEL}", headers=headers, json=json_data)
    try:
        return r.json()[0]['generated_text']
    except:
        return "Sorry, couldn't generate response."

@bot.message_handler(func=lambda m: True)
def chat_with_hf(msg):
    reply = query_hf(msg.text)
    bot.reply_to(msg, reply)

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
