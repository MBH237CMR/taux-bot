import os
import telebot
import requests
from datetime import datetime

# Récupère les secrets GitHub
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# Vérif rapide
if not TOKEN:
    print("❌ TELEGRAM_TOKEN manquant")
    exit(1)
if not CHANNEL_ID:
    print("❌ TELEGRAM_CHANNEL_ID manquant") 
    exit(1)

bot = telebot.TeleBot(TOKEN)

def get_taux_cad_xaf():
    """Récupère le taux CAD→XAF via API gratuite exchangerate-api"""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/CAD"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        taux = data['rates']['XAF']
        print(f"Taux récupéré: 1 CAD = {taux} XAF")
        return float(taux)
    except Exception as e:
        print(f"❌ Erreur API taux: {e}")
        return None

def send_to_telegram():
    taux = get_taux_cad_xaf()
    date_heure = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    if taux is None:
        message = f"""❌ Erreur récupération taux

Impossible de récupérer le taux CAD→XAF pour le moment.
Réessai au prochain cycle.

📅 {date_heure}"""
    else:
        calc_100 = taux * 100
        calc_500 = taux * 500
        calc_1000 = taux * 1000
        
        message = f"""💱 Taux de change CAD → XAF

1 CAD = {taux:.2f} XAF

💰 Equivalences rapides:
100 CAD = {calc_100:.0f} XAF
500 CAD = {calc_500:.0f} XAF  
1000 CAD = {calc_1000:.0f} XAF

📅 Mis à jour: {date_heure}
📊 Source: exchangerate-api.com"""

    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print(f"✅ Message envoyé avec succès au canal {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Erreur envoi Telegram: {e}")
        exit(1)

if __name__ == "__main__":
    print(f"Token chargé: {TOKEN[:8]}...")
    print(f"Channel ID: {CHANNEL_ID}")
    send_to_telegram()
