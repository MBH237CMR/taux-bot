import os
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_rate():
    url = "https://api.exchangerate-api.com/v4/latest/CAD"
    r = requests.get(url).json()
    rate = r["rates"]["XAF"]
    return rate

def send_message():
    rate = get_rate()
    text = f"💱 Taux CAD → XAF\n1 CAD = {rate:.2f} XAF"
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHANNEL_ID, text=text)

if __name__ == "__main__":
    send_message()
