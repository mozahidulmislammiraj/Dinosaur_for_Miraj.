import os
import telebot
import requests

HF_API_KEY = os.getenv("HF_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

MODEL = "gpt2"  # অথবা "TheBloke/WizardLM-7B-1.0-HF" (CPU-friendly)

def ask_hf(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    r = requests.post(f"https://api-inference.huggingface.co/models/{MODEL}", headers=headers, json=payload)
    return r.json()[0]["generated_text"]

@bot.message_handler(func=lambda message: True)
def reply(message):
    response = ask_hf(message.text)
    bot.reply_to(message, response)

bot.polling()