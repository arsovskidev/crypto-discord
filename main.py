import os
from dotenv import load_dotenv
import random
import datetime
import pytz
import requests
from urllib import parse
import time
import math
import json

# Load environment (.env) settings.
load_dotenv()
TIMEZONE = os.getenv("TIMEZONE")
EXCHANGE_RATES_API = os.getenv("EXCHANGE_RATES_API")
GIPHY_API = os.getenv("GIPHY_API")
DISCORD_TRX = os.getenv("DISCORD_TRX")
DISCORD_SOL = os.getenv("DISCORD_SOL")

conf = {
    'tron': {
        'url': DISCORD_TRX,
        'color': 16711680,
    },
    'solana': {
        'url': DISCORD_SOL,
        'color': 4902143,
    },
}

# Threshold settings.
threshold = {
    "tron": {"MAX": 0.00, "MIN": 0.00},
    "solana": {"MAX": 0.00, "MIN": 0.00},
}
gif_keywords = {
    "good": [
        'rocket launch',
        'to the moon',
    ],
    "bad": [
        'sad',
        'crying',
        'rocket crash',
    ]
}
# Loop interval
time_interval = 60 * 10


def sendMessage(head, body, coin, gif):
    url = conf[coin]['url']
    color = conf[coin]['color']
    timezone = pytz.timezone(TIMEZONE)
    date = datetime.datetime.now(timezone).isoformat()
    data = {
        "embeds": [
            {
                "title": head,
                "color": color,
                "fields": [
                    {
                    "name": "Information",
                    "value": body
                    }
                ],
                "footer": {
                    "text": "Astennu System",
                    "icon_url": "https://avatars.githubusercontent.com/u/74111156?v=4"
                },
                "timestamp": date,
                "image": {}
            }
        ]
    }
    if gif:
        data['embeds'][0]['image']['url'] = gif

    requests.post(url, json = data)

def getValue(coin, fiat):
    url = f"{EXCHANGE_RATES_API}ids={coin}&vs_currencies={fiat}"
    response = requests.get(url)
    response_json = response.json()
    price = float(response_json[coin][fiat])
    return price

def getGifUrl(type):
    keyword = random.choice(gif_keywords[type])
    print(keyword)
    url = "http://api.giphy.com/v1/gifs/search"
    params = parse.urlencode({
        "q": keyword,
        "api_key": GIPHY_API,
        "limit": "1"
    })
    gif = requests.get(url, params)
    gif = gif.json()
    gif_url = gif['data'][0]['images']['original']['url']
    return gif_url

def updateThreshold(coin, type, value):
    if coin == "tron":
        if type == "MAX":
            threshold[coin][type] = value + 0.01
        elif type == "MIN":
            threshold[coin][type] = value - 0.01
    elif coin == "solana":
        if type == "MAX":
            threshold[coin][type] = value + 30.00
        elif type == "MIN":
            threshold[coin][type] = value - 30.00

def calibrateThreshold(coin, fiat):
    price = getValue(coin, fiat)
    price = round(price, 2)
    updateThreshold(coin, "MAX", price)
    updateThreshold(coin, "MIN", price)

def checkCoin(coin, fiat):
    price = getValue(coin, fiat)
    threshold_max = threshold[coin]["MAX"]
    threshold_min = threshold[coin]["MIN"]

    if price >= threshold_max:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'{coin.upper()} Rise Signal 📈',
            f'​Current price: `{price}` _{fiat.upper()}_\nCurrent threshold: `{round(threshold_max, 2)}` _{fiat.upper()}_\nCalibrated threshold: `{round(threshold[coin]["MAX"], 2)}` _{fiat.upper()}_',
            coin,
            getGifUrl("good")
        )

    elif price <= threshold_min:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'{coin.upper()} Down Signal 📉',
            f'​Current price: `{price}` _{fiat.upper()}_\nCurrent threshold: `{round(threshold_min, 2)}` _{fiat.upper()}_\nCalibrated threshold: `{round(threshold[coin]["MIN"], 2)}` _{fiat.upper()}_',
            coin,
            getGifUrl("bad")
        )

# -----------------------------------------------------------------
# Main Loop

calibrateThreshold('tron', 'eur')
calibrateThreshold('solana', 'eur')

def main():
    while True:
        print("Getting DATA...")

        checkCoin("tron", "eur")
        checkCoin("solana", "eur")

        time.sleep(time_interval)


if __name__ == "__main__":
    main()