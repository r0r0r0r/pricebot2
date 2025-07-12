import requests
import schedule
import time
from datetime import datetime

# 🧠 Memory to track last prices
last_prices = {}

# 📝 Log file
LOG_FILE = "alerts_log.txt"

# 📲 Telegram credentials
TELEGRAM_BOT_TOKEN = "7063080355:AAHIHHhl28YDQd6bwjGw3NR0XlncK6K5FH4"
TELEGRAM_CHAT_ID = "7627934353"

# 📩 Send Telegram alert
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("❌ Failed to send:", response.text)

# 💾 Save alert to file
def log_alert(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# 🔍 Check prices for unusual movement
def check_prices():
    try:
        response = requests.get("https://api.coindcx.com/exchange/ticker")
        data = response.json()

        for item in data:
            symbol = item["market"]
            current_price = float(item["last_price"])

            if symbol in last_prices:
                prev_price = last_prices[symbol]
                percent_change = ((current_price - prev_price) / prev_price) * 100

                if abs(percent_change) >= 5:
                    direction = "🔺 Spiked" if percent_change > 0 else "🔻 Crashed"
                    msg = (
                        f"⚠️ {direction} fast!\n"
                        f"{symbol}\n"
                        f"Now: ₹{current_price:.6f}\n"
                        f"Change: {percent_change:.2f}% in 5 seconds"
                    )
                    send_telegram_message(msg)
                    log_alert(f"{symbol} | {direction} {percent_change:.2f}%")

            last_prices[symbol] = current_price

    except Exception as e:
        print("❗ Error checking prices:", e)

# 🔁 Run every 5 seconds instead of 1 minute
schedule.every(5).seconds.do(check_prices)

print("📡 CoinDCX Bot Running... Monitoring all coins every 5 seconds...")

# 🌀 Keep running forever
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting
 