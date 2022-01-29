# Crypto-Discord

![](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Farshetamine%2Fcrypto-discord&count_bg=%23A4B6F7&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

#### Discord Webhooks for alerting crypto currency price changes &amp; historical data.

###### Create virtual environment and install requirements.

```
$ sudo apt-get install python3-venv
$ python3 -m venv crypto-discord
$ source crypto-discord/bin/activate
$ touch .env
$ pip3 install -r requirements.txt
$ python3 main.py
```

###### In the .env file enter the following settings.

```
$ nano .env

EXCHANGE_RATES_API = 'https://api.coingecko.com/api/v3/simple/price?'
DISCORD_TRX = [YOUR WEBHOOK FOR TRON ALERTS]
DISCORD_SOL = [YOUR WEBHOOK FOR SOLANA ALERTS]

```
