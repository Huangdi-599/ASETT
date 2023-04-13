import requests
from decimal import Decimal
from django.db.utils import IntegrityError
from .models import Crypto
from apscheduler.schedulers.background import BackgroundScheduler
import time

scheduler = BackgroundScheduler()


def Crypto_data():
    data = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en').json()

    for item in data:
        try:
            crypto = Crypto.objects.get(name=item['name'])
            crypto.symbol = item['symbol']
            crypto.price = Decimal(str(item['current_price']))
            crypto.market_cap = item['market_cap']
            crypto.percentage_change = Decimal(str(item['price_change_percentage_24h']))
            crypto.save()
        except Crypto.DoesNotExist:
            Crypto.objects.create(
                name=item['name'],
                symbol=item['symbol'],
                price=Decimal(str(item['current_price'])),
                market_cap=item['market_cap'],
                percentage_change=Decimal(str(item['price_change_percentage_24h']))
            )
        except IntegrityError:
            # handle duplicates here
            pass

scheduler.add_job(Crypto_data, 'interval', seconds=120)
scheduler.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()