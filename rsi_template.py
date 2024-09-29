import time
import subprocess
import requests
import sys

# Replace with your API secret (register for free account, limit rate on 15s)
API_URL = "https://api.taapi.io/rsi"
API_SECRET = "<API_SECRET>"
EXCHANGE = "binance"
SYMBOL = "BTC/USDT"
INTERVAL = "1h"

# Enter your Telegram bot details (use @botfarther to get bot token)
TELEGRAM_BOT_TOKEN = "<BOT_TOKEN>"
TELEGRAM_CHAT_ID = "<CHAT_ID>"
USERNAME = 'alvosecbot'

def get_rsi_value():
    params = {
        "secret": API_SECRET,
        "exchange": EXCHANGE,
        "symbol": SYMBOL,
        "interval": INTERVAL
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("value")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSI value: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def send_telegram_notification(message):
    try:
        if "successfully" in message.lower():
            telegram_url = f"https://api.telegram.org/{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "disable_notification": False
            }
            response = requests.post(telegram_url, json=payload)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram notification: {e}")
        
def get_trade_details():
    url = f"https://mainnet.api.protondex.com/dex/v1/trades/history?account={USERNAME}&symbol=XBTC_XMD&limit=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("count", 0) > 0:
            trade_data = data["data"][0]
            trade_id = trade_data["trade_id"]
            price = trade_data["price"]
            trx_id = trade_data["trx_id"]
            return f"Trade ID: {trade_id}, Price: {price}, Transaction: https://explorer.xprnetwork.org/transaction/{trx_id}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trade details: {e}")
    except Exception as e:
        print(f"An error occurred while fetching trade details: {e}")
    return None

def place_sell():
    print("Placing sell order...")
    result = subprocess.run(["python3", "dex_bot.py", "sell"], capture_output=True, text=True)
    if "Error" not in result.stdout:
        print("Sell order placed successfully.")
        trade_details = get_trade_details()
        if trade_details:
            print("Trade Details:", trade_details)
            send_telegram_notification(f" 🤖 Sell order placed successfully.\n\n{trade_details}")
        else:
            send_telegram_notification("Sell order placed successfully.")
    else:
        print("Error placing sell order:", result.stdout)

def place_buy():
    print("Placing buy order...")
    result = subprocess.run(["python3", "dex_bot.py", "buy"], capture_output=True, text=True)
    if "Error" not in result.stdout:
        print("Buy order placed successfully.")
        trade_details = get_trade_details()
        if trade_details:
            print("Trade Details:", trade_details)
            send_telegram_notification(f" 🤖 Buy order placed successfully.\n\n{trade_details}")
        else:
            send_telegram_notification("Buy order placed successfully.")
    else:
        print("Error placing buy order:", result.stdout)


def main():
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "sell":
            place_sell()
        elif action == "buy":
            place_buy()
        else:
            print("Invalid action. Use 'sell' or 'buy'.")
    else:
        while True:
            try:
                rsi_value = get_rsi_value()

                if rsi_value is not None:
                    print(f"Current RSI value: {rsi_value}")

                    if rsi_value > 70:
                        print("RSI is greater than 70. Calling script to sell...")
                        place_sell()

                    elif rsi_value < 30:
                        print("RSI is less than 30. Calling script to buy...")
                        place_buy()

                    else:
                        print("Nothing to trade...")
            except Exception as e:
                print(f"An error occurred: {e}")
                send_telegram_notification(f"This is an automatic warning: An error occurred in the trading script: {e}")

            time.sleep(300) # Change time interval of this script

if __name__ == "__main__":
    main()
