# XPRNetwork-Trading-Bot

> [!CAUTION]
> Caution: This bot is provided for educational purposes only. Use it at your own risk and exercise caution when trading with real funds. We advise starting with a small balance to gain experience with bot trading and to understand the risks involved.

This repository contains a trading bot designed for the [XPR Network](https://xprnetwork.org/). The bot automates buying and selling actions based on the RSI (template file) value fetched from an external API. The bot also integrates with the MetalX DEX for placing orders and supports notifications via Telegram.

The RSI template file serves as an **example** of how to retrieve the RSI value for the **BTC/USDT** pair using the TAAPI service. In the future there will be more indicators included as template files.

The `dex_bot.py` file is the core script used to place orders on the [MetalX DEX](https://app.metalx.com). The template file serves as a runnable script that interacts with `dex_bot.py` to execute trades.

```
usage: dex_bot.py [-h] [--panic-sell] [--percentage {25,50,75,100}] {buy,sell}

Buy or sell XMD or XBTC

positional arguments:
  {buy,sell}            Specify the action (buy or sell) If (buy) is used script will purchase XBTC using XMD. If (sell)
                        is used then XBTC will be sold to XMD.

optional arguments:
  -h, --help            show this help message and exit
  --panic-sell          Flag to perform panic sell
  --percentage {25,50,75,100}
                        Percentage of total balance to buy/sell (25, 50, 75, 100)
```

## How to install this bot?

This instructions are suitable for a Linux distribution like **Ubuntu 22.04**:

Install **Python3** and **pip**:
```
sudo apt-get install python3 python3-pip -y
```
Install System Dependencies for **pyeoskit**:

```
sudo apt-get install git build-essential libssl-dev libffi-dev python3-dev -y
```

Install Required Python Packages:

```
pip3 install requests pyeoskit argparse configparser
```

Clone the Repository:

```
git clone https://github.com/alvosec/XPRNetwork-Trading-Bot.git
cd XPRNetwork-Trading-Bot
```

Setup Environment:

Insert your private key and username into `config.ini`:

```
[credentials]
private_key = your_private_key_here
username = alvosecbot
```

> [!IMPORTANT]  
> We recommend creating a new WebAuth account specifically for trading purposes.

## How to use this bot?

You can now run the `dex_bot.py` script using the `--help` option.

> [!NOTE]  
> Keep in mind that this BOT only uses market orders.

If you want to buy XBTC you will perform this command:

`python3 dex_bot.py buy`

If you have no balance you will get:

`Error: XMD balance not found or insufficient balance.`

You can also use `--percentage` option, to define total balance to buy or sell.

`python3 dex_bot.py --percentage 25 buy`

Successful trade:

```
Quantity: 2.477959 XMD
{'sync': 273918047, 'data': {'trx_id': 'd648babd1da1fcec7dd489546ba56fff43546812587c370c787b2436c2669c14', 'block_time': '2024-08-25T23:28:27.000Z', 'orders': [{'ordinal_order_id': '0789efe2e13e3fd20ac7f948c4e7b8b188fbed41983c7a1bb2c84b449556670f', 'order_id': '17391028', 'status': 'create'}]}}
```

Then you can perform sell action to sell all my XBTC:

`python3 dex_bot.py --percentage 100 sell`

Response:

```
Quantity: 0.00003825 XBTC
{'sync': 273918210, 'data': {'trx_id': '5b84cb0bff72aee3b83b50f2aa0c41012f33e77a7dc302fc6a7ed7386129a3cf', 'block_time': '2024-08-25T23:29:48.000Z', 'orders': [{'ordinal_order_id': '651d8bcd03f8001c9613c8ddef3e8f5bc7bbbd66c757ace00dd6b102e722b8e9', 'order_id': '17391037', 'status': 'create'}]}}
```

> [!TIP]
> This trading bot can be run (24/7/365) on a simple & cheap VPS on Hetzner. [Hetzner Cloud](https://hetzner.cloud/?ref=nmlWJ6LYypzX)

If you want to change the BID_TOKEN from XBTC to another cryptocurrency, you will need to modify this part of the script:

```
BID_TOKEN_CONTRACT = 'xtokens'
BID_TOKEN_SYMBOL = 'XBTC'
BID_TOKEN_PRECISION = 8
```
Below is a list of supported token contracts and their token precision that you can change:

```
const BID_TOKEN_CONTRACT = 'eosio.token'
const BID_TOKEN_SYMBOL = 'XPR'
const BID_TOKEN_PRECISION = 4

const BID_TOKEN_CONTRACT = 'xtokens'
const BID_TOKEN_SYMBOL = 'XETH'
const BID_TOKEN_PRECISION = 8

const BID_TOKEN_CONTRACT = 'xtokens'
const BID_TOKEN_SYMBOL = 'METAL'
const BID_TOKEN_PRECISION = 8

const BID_TOKEN_CONTRACT = 'xtokens'
const BID_TOKEN_SYMBOL = 'XDOGE'
const BID_TOKEN_PRECISION = 6

const BID_TOKEN_CONTRACT = 'xtokens'
const BID_TOKEN_SYMBOL = 'XLTC'
const BID_TOKEN_PRECISION = 8
```

These are some of the supported currencies, but MetalX supports more, which are available at: https://app.metalx.com/dex/XPR_XMD

## How to run BOT template?

> [!NOTE]  
> You can create your own template that will call the `dex_bot.py` file to execute orders.

This trading bot utilizes the [Taapi.io](https://taapi.io/) RSI API to monitor the Relative Strength Index (RSI) values for a specified cryptocurrency.

```
API_URL = "https://api.taapi.io/rsi"
API_SECRET = "<API_SECRET>"
EXCHANGE = "binance"
SYMBOL = "BTC/USDT"
INTERVAL = "1h"
```

You also have the option to receive Telegram notifications when a trade is successfully executed.

```
TELEGRAM_BOT_TOKEN = "<BOT_TOKEN>"
TELEGRAM_CHAT_ID = "<CHAT_ID>"
USERNAME = 'alvosecbot' # Change to your username
```

To run the `rsi_template.py` script in the background, you can use the following command:

`nohup python3 rsi_template.py &`

RSI template makes API requests in a loop that executes every 5 minutes (300 seconds):

`time.sleep(300)  # Change time interval of this script`

We encourage you to experiment with the bot, make improvements, and contribute to its development. Happy trading!
