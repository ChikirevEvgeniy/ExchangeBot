import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise  APIException(f'Не удалось обработать количество {amount}!')


        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}"
        payload = {}
        headers = {
            "apikey": "qK0ku6fr8o1lunePaQtp5zSGvl47Duok"
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * float(amount)
        return new_price