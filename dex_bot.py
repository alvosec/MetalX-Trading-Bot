"""
Author: Alvosec
Website: https://alvosec.com
Email: info@alvosec.com

Caution: This script is provided for educational purposes only. 
         Use it at your own risk and exercise caution when trading 
         with real funds. We advise starting with a small balance 
         to gain experience with bot trading and understand the risks involved.
"""

import os
import json
import requests
from pyeoskit import eosapi, wallet
from math import pow
import argparse
import configparser

# Load private key from config file
config = configparser.ConfigParser()
config.read('config.ini')

PRIVATE_KEY = config.get('credentials', 'private_key')

# Keep your private key safe and follow our blog at https://alvosec.com/blog
wallet.import_key('alvosecbot', PRIVATE_KEY)

eosapi.set_node('https://mainnet-rpc.api.protondex.com')

# Make sure to change username to your account
USERNAME = 'alvosecbot'
permission = {USERNAME: 'active'}

url = "https://mainnet.api.protondex.com/dex/v1/orders/submit"
headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

BID_TOKEN_CONTRACT = 'xtokens'
BID_TOKEN_SYMBOL = 'XBTC'
BID_TOKEN_PRECISION = 8

ASK_TOKEN_CONTRACT = 'xmd.token'
ASK_TOKEN_SYMBOL = 'XMD'
ASK_TOKEN_PRECISION = 6

MARKET_ID = 2  # Unique ID of market
FILL_TYPE = 1  # IOC (Immediate-Or-Cancel)

parser = argparse.ArgumentParser(description='Buy or sell XMD or XBTC')
parser.add_argument('action', choices=['buy', 'sell'], help='Specify the action (buy or sell) If (buy) is used script will purchase XBTC using XMD. If (sell) is used then XBTC will be sold to XMD.')
parser.add_argument('--panic-sell', action='store_true', help='Flag to perform panic sell')
parser.add_argument('--percentage', type=int, choices=[25, 50, 75, 100], default=100, help='Percentage of total balance to buy/sell (25, 50, 75, 100)')
args = parser.parse_args()

if args.action == 'buy':
    ORDER_TYPE = 1
    ORDER_SIDE = 1  # Buy (1)
    TOKEN_CONTRACT = ASK_TOKEN_CONTRACT
    TOKEN_SYMBOL = ASK_TOKEN_SYMBOL
    TOKEN_PRECISION = ASK_TOKEN_PRECISION
else:
    ORDER_TYPE = 1
    ORDER_SIDE = 2  # Sell (2)
    TOKEN_CONTRACT = BID_TOKEN_CONTRACT
    TOKEN_SYMBOL = BID_TOKEN_SYMBOL
    TOKEN_PRECISION = BID_TOKEN_PRECISION

account_balance_url = "https://mainnet.api.protondex.com/dex/v1/account/balances"
balance_response = requests.get(f"{account_balance_url}?account={USERNAME}")
balance_data = balance_response.json()

ORDER_AMOUNT = None
for balance_item in balance_data.get("data", []):
    if balance_item.get("currency") == TOKEN_SYMBOL:
        ORDER_AMOUNT = int(float(balance_item.get("amount")) * pow(10, TOKEN_PRECISION))
        break

if ORDER_AMOUNT is None or ORDER_AMOUNT == 0:
    print(f"Error: {TOKEN_SYMBOL} balance not found or insufficient balance.")
    exit(1)

percentage_to_use = args.percentage / 100.0
buy_amount = int(ORDER_AMOUNT * percentage_to_use)

if args.panic_sell and args.action == 'sell':
    ORDER_AMOUNT = buy_amount
else:
    ORDER_AMOUNT = buy_amount

args1 = {
    'from': USERNAME,
    'to': 'dex',
    'quantity': f'{ORDER_AMOUNT / pow(10, TOKEN_PRECISION):.{TOKEN_PRECISION}f} {TOKEN_SYMBOL}',
    'memo': ''
}

args2 = {
    'market_id': MARKET_ID,
    'account': USERNAME,
    'order_type': ORDER_TYPE,
    'order_side': ORDER_SIDE,
    'fill_type': FILL_TYPE,
    'bid_symbol': {
        'sym': f'{BID_TOKEN_PRECISION},{BID_TOKEN_SYMBOL}',
        'contract': BID_TOKEN_CONTRACT
    },
    'ask_symbol': {
        'sym': f'{ASK_TOKEN_PRECISION},{ASK_TOKEN_SYMBOL}',
        'contract': ASK_TOKEN_CONTRACT
    },
    'referrer': '',
    'quantity': ORDER_AMOUNT,
    'price': 1 if args.action == 'sell' else int(9223372036854775806),
    'trigger_price': 0
}

args3 = {
    'q_size': 20,
    'show_error_msg': 0
}

a1 = [TOKEN_CONTRACT, 'transfer', args1, permission]
a2 = ['dex', 'placeorder', args2, permission]
a3 = ['dex', 'process', args3, permission]

info = eosapi.get_info()
final_tx = eosapi.generate_packed_transaction(
    [a1, a2, a3],
    60,
    info['last_irreversible_block_id'],
    info['chain_id']
)
mtx = json.loads(final_tx)

print(f"Quantity: {ORDER_AMOUNT / pow(10, TOKEN_PRECISION):.{TOKEN_PRECISION}f} {TOKEN_SYMBOL}")

payload = {
    "serialized_tx_hex": mtx["packed_trx"],
    "signatures": mtx["signatures"]
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(data)
