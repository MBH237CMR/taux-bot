import os
import telebot
import requests
import math
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
bot = telebot.TeleBot(TOKEN)

def arrondi_perso(valeur):
    """Règle maison : 411,05→411 | 411,06→412 | 411,07→412"""
    entiere = math.floor(valeur)
    decimale = valeur - entiere
    return entiere + 1 if decimale >= 0.06 else entiere

def get_taux_cad_xaf():
    """Taux API + 0.7% + arrondi perso"""
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/CAD", timeout=15)
        r.raise_for_status()
        taux_base = float(r.json()['rates']['XAF'])
        taux_final = arrondi_perso(taux_base * 1.007)
        print(f"Base: {taux_base} | Final: {taux_final}")
        return taux_final
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def send_to_telegram():
    taux = get_taux_cad_xaf()
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    if taux is None:
        msg = f"❌ Erreur taux\n{date}"
    else:
        msg = f"""💱 Taux CAD → XAF

1 CAD = {taux} XAF

💰 100 CAD = {arrondi_perso(taux * 100)} XAF
💰 500 CAD = {arrondi_perso(taux * 500)} XAF
💰 1000 CAD = {arrondi_perso(taux * 1000)} XAF

📅 {date}"""

    bot.send_message(chat_id=CHANNEL_ID, text=msg)
    print("Message envoyé")

if __name__ == "__main__":
    send_to_telegram()
