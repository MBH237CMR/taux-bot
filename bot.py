import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("Token présent:", bool(TELEGRAM_TOKEN))
print("Chat ID présent:", bool(TELEGRAM_CHAT_ID))

def get_tx():
    r = requests.get("https://api.exchangerate-api.com/v4/latest/CAD", timeout=10)
    r.raise_for_status()
    rate = r.json()["rates"]["XAF"]
    return rate * 1.0055

def main():
    tx = get_tx()
    msg = f"""🇨🇦🇨🇲Taux de change Live🇨🇦🇨🇲

1 CAD = {tx:.2f} CFA

100 CAD = {tx*100:.0f} CFA

500 CAD = {tx*500:.0f} CFA"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}  # sans parse_mode pour tester
    
    res = requests.post(url, json=payload)
    print("Status Telegram:", res.status_code)
    print("Réponse Telegram:", res.text)

if __name__ == "__main__":
    main()
