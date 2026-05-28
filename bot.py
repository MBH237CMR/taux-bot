import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_google_rate():
    url = "https://api.exchangerate-api.com/v4/latest/CAD"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()["rates"]["XAF"]

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Token ou Chat ID manquant")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    print(f"Status: {r.status_code}")

def main():
    rate_google = get_google_rate()
    
    # Calcul interne: +1.06% SANS arrondi
    tx = rate_google * 1.0109
    
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Affichage client: max 2 décimales
    message = f"<b>💱 Taux CAD → XAF {date_now}</b>\n\n"
    message += f"🇨🇦 1 CAD = <b>{tx:.2f} XAF</b> 🇨🇲\n"
    message += f"🇨🇦 100 CAD = <b>{tx * 100:.2f} XAF</b> 🇨🇲\n"
    message += f"🇨🇦 500 CAD = <b>{tx * 500:.2f} XAF</b> 🇨🇲"
    
    send_telegram(message)
    print(f"Taux Google API: {rate_google} | Taux calculé +1.06%: {tx} | Envoyé: {tx:.2f}")

if __name__ == "__main__":
    main()
