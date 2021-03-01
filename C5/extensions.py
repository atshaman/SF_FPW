# -*- coding: utf-8 -*-

"""Определение классов для проекта 'телеграм-бот' """

import requests
import datetime


class ApiException(Exception):
    pass


class GetCurrency:
    def __init__(self, cache=None):
        self.url = 'https://api.exchangeratesapi.io'
        if cache:
            self.cache = datetime.timedelta(seconds=cache)
            self.refresh()
        else:
            self.cache = None

    def refresh(self):
        self.refresh = datetime.datetime.now()
        try:
            self.cvalues = requests.get(self.url + '/latest').json()['rates']
        except Exception:
            raise ApiException('Ошибка получения данных о курсе валют по сети!')
        # Явным образом добавляем базу рассчета
        self.cvalues['EUR'] = 1

    def get_price_cache(self, base: str, quote: str, amount: int) -> float:
        if (self.cache is None) or (datetime.datetime.now() - self.refresh > self.cache):
            self.refresh()
        if self.cvalues.get(base.capitalize(), None) is None:
            raise ApiException(f'Базовая валюта {base} отсутствует в списке доступных для конвертации!')
        if self.cvalues.get(quote.capitalize(), None) is None:
            raise ApiException(f'Результирующая валюта {quote} отсутствует в списке доступных для конвертации!')
        if amount <= 0:
            raise ApiException(f'Количество обмениваемой валюты должно быть целым положительным числом > 0!')
        base = self.cvalues.get(base)
        quote = self.cvalues.get(quote)
        return amount / base * quote

    @staticmethod
    def get_price(base, quote, amount):
        pass


if __name__ == '__main__':
    # Unit-тест на минималках
    exchange = GetCurrency(cache=None)
    print(exchange.get_price_cache('EUR', 'RUB', 100))
