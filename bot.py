import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_tx():
    # API plus stable : exchangerate-api.com
    url = "https://api.exchangerate-api.com/v4/latest/CAD"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    
    # Sécurité si l’API répond mal
    if "rates" not in data or "XAF" not in data["rates"]:
        raise ValueError(f"API a renvoyé: {data}")
    
    rate_google = float(data["rates"]["XAF"])
    
    # Tx = Taux Google + 0,55%
    tx = rate_google * 1.0055
    return tx

def main():
    tx = get_tx()
    
    msg = f"""🇨🇦🇨🇲Taux de change Live🇨🇦🇨🇲
           💰 ♻️💲

_*1 CAD = {tx:.2f} CFA*_

_*100 CAD = {tx*100:.0f} CFA*_

_*500 CAD = {tx*500:.0f} CFA*_

          💱 💰 💱 _XAF_"""
    
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    )

if __name__ == "__main__":
    main()
