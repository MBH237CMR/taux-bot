import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # ta discussion privée
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # nouveau: ID du canal

def get_google_rate():
    url = "https://api.exchangerate-api.com/v4/latest/CAD"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()["rates"]["XAF"]

def send_telegram(message, chat_id):
    if not TELEGRAM_TOKEN or not chat_id:
        print("Token ou Chat ID manquant")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    print(f"Envoi vers {chat_id}: Status {r.status_code}")

def main():
    rate_google = get_google_rate()
    tx = rate_google * 1.0106  # 1.06%
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    message = f"<b>💱 Taux CAD → XAF {date_now}</b>\n\n"
    message += f"🇨🇦 1 CAD = <b>{tx:.2f} XAF</b> 🇨🇲\n"
    message += f"🇨🇦 100 CAD = <b>{tx * 100:.2f} XAF</b> 🇨🇲\n"
    message += f"🇨🇦 500 CAD = <b>{tx * 500:.2f} XAF</b> 🇨🇲"
    
    # Envoie à toi
    send_telegram(message, TELEGRAM_CHAT_ID)
    # Envoie au canal
    send_telegram(message, TELEGRAM_CHANNEL_ID)

if __name__ == "__main__":
    main()
