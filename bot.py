import os
import requests
from datetime import datetime
import math

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_CHANNEL_ID = os.getenv('WHATSAPP_CHANNEL_ID')

bot = requests.Session()

def arrondi_perso(valeur):
    """Arrondi perso : <1000 = 0 décimales, >=1000 = pas de décimales"""
    if valeur < 1000:
        return round(valeur)
    return int(valeur)

def get_taux_cad_xaf():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/CAD"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data['rates']['XAF']
    except:
        return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHANNEL_ID, "text": msg}
    try:
        requests.post(url, data=data, timeout=10)
        print("Telegram OK")
    except Exception as e:
        print(f"Erreur Telegram: {e}")

def send_whatsapp_channel(msg):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_CHANNEL_ID,
        "type": "text",
        "text": {"body": msg}
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=15)
        print(f"WhatsApp Channel: {r.status_code}")
    except Exception as e:
        print(f"Erreur WhatsApp: {e}")

def main():
    taux = get_taux_cad_xaf()
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    if taux is None:
        msg = f"❌ Erreur récupération taux\n📅 {date}"
    else:
        msg = f"""💱 Taux CAD → XAF

1 CAD = {taux:.2f} XAF

💰 100 CAD = {arrondi_perso(taux * 100)} XAF
💰 500 CAD = {arrondi_perso(taux * 500)} XAF  
💰 1000 CAD = {arrondi_perso(taux * 1000)} XAF

📅 {date}"""

    send_telegram(msg)
    send_whatsapp_channel(msg)

if __name__ == "__main__":
    main()
