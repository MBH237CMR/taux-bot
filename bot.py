import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_google_rate():
    """Récupère taux CAD->XAF depuis Google via exchangerate-api gratuit"""
    url = "https://api.exchangerate-api.com/v4/latest/CAD"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data["rates"]["XAF"]
    except Exception as e:
        print(f"Erreur récupération taux: {e}")
        return None

def send_telegram(message):
    """Envoie message sur Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Token présent:", bool(TELEGRAM_TOKEN), "Chat ID présent:", bool(TELEGRAM_CHAT_ID))
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Status Telegram: {r.status_code}")
        print(f"Réponse Telegram: {r.text[:200]}")
        return r.status_code == 200
    except Exception as e:
        print(f"Erreur envoi Telegram: {e}")
        return False

def main():
    # 1. Récupère taux Google
    rate_google = get_google_rate()
    if not rate_google:
        send_telegram("❌ Erreur: Impossible de récupérer le taux Google")
        return
    
    # 2. Applique ta formule: Tx = Taux Google + 0,55%(Taux Google)
    margin = 0.0055  # 0.55%
    tx = rate_google * (1 + margin)
    
    # 3. Arrondi à 2 décimales
    rate_google = round(rate_google, 2)
    tx = round(tx, 2)
    
    # 4. Message Telegram
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f"<b>💰 Taux CAD → XAF du {date_now}</b>\n\n"
    message += f"Taux Google: <code>{rate_google} XAF</code>\n"
    message += f"Notre taux +0.55%: <b>{tx} XAF</b>\n\n"
    message += f"Marge appliquée: +0.55%"
    
    # 5. Envoi
    send_telegram(message)
    print(f"Taux envoyé: Google={rate_google} | Notre taux={tx}")

if __name__ == "__main__":
    main()
