import os
import requests
from bs4 import BeautifulSoup
import telebot
from datetime import datetime

# Récupère les secrets GitHub
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  # Ton ID perso pour les tests
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')  # -1004220934501

bot = telebot.TeleBot(TOKEN)

def get_taux_cad_xaf():
    """Récupère le taux CAD vers XAF - adapte l'URL selon ta source"""
    try:
        url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=CAD&To=XAF"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Adapte le sélecteur selon le site que tu scrapes
        taux = soup.find('p', {'class': 'result__BigRate-sc-1bsijpp-1'}).text.strip()
        return taux
    except:
        return "Erreur récupération taux"

def send_to_telegram(message):
    """Envoie à toi + au canal"""
    try:
        # 1. Envoi en privé pour test
        if CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
            print(f"Envoyé à CHAT_ID: {CHAT_ID}")
        
        # 2. Envoi dans le canal - LA LIGNE CLÉ
        if CHANNEL_ID:
            bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
            print(f"Envoyé au canal: {CHANNEL_ID}")
            
    except Exception as e:
        print(f"Erreur Telegram: {e}")

if __name__ == "__main__":
    taux = get_taux_cad_xaf()
    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    message = f"""💱 <b>Taux CAD → XAF Live</b> 💱
    
1 CAD = {taux} XAF

📅 Mise à jour: {date}
#CADCFA #TauxDuJour"""
    
    send_to_telegram(message)
    print("Terminé !")
