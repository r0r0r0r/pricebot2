import requests

BOT_TOKEN = "7063080355:AAHIHHhl28YDQd6bwjGw3NR0XlncK6K5FH4"
CHAT_ID = "7627934353"
msg = "✅ Test alert from your CoinDCX bot!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": msg}

r = requests.post(url, data=data)
print("✅ Test sent! Check your Telegram.")
