import requests
import json
import math
from config import APIKEY, keys

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f"Неверный параметр количества {amount}!")

        try:
            base_simb = keys[base]
        except KeyError:
            raise ApiException(f"Валюта {base} не найдена!")

        try:
            quote_simb = keys[quote]
        except KeyError:
            raise ApiException(f"Валюта {quote} не найдена!")

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote} в {quote}!')

        pair = ''.join((base_simb, quote_simb))

        r = requests.get(f'https://currate.ru/api//?get=rates&pairs={pair}&key={APIKEY}')
        rates = json.loads(r.content)

        return round(float(rates['data'][pair])*amount, 2)