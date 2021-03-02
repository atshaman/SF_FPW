# -*- coding: utf-8 -*-

"""Определение классов для проекта 'телеграм-бот' """

import requests
import datetime
import telebot


class ApiException(Exception):
    pass


class GetCurrency:
    VALUES = {'CAD': "Canadian Dollars", 'HKD': "HongKong Dollars", 'ISK': "Islandic Krona", 'PHP': "Philippine Peso",
              'DKK': "Danish Krone", 'HUF': "Hungarian Forint", 'CZK': "Czech koruna", 'AUD': "Australian Dollar",
              'RON': "Romanian Leu", 'SEK': "Swedish Krona", 'IDR': "Indonesian Rupiah", 'INR': "Indian Rupee",
              'BRL': "Brazilian real", 'RUB': "Russian Rubles", 'HRK': 'Kroatian Kuna', 'JPY': "Japanese Yen",
              'THB': "Thai Baht", 'CHF': "Swiss Frank", 'SGD': "Singapore dollar", 'PLN': "Polish Zloty",
              'BGN': "Bulgarian Lev", 'TRY': "Turkish Lira", 'CNY': "Chinese Yuan Renminbi", 'NOK': "Norwegian krone",
              'NZD': "New Zealand Dollar", 'ZAR': "South African Rand", 'USD': "United States Dollars",
              'MXN': "Mexican Peso", 'ILS': "Israeli New Shekel", 'GBP': "British Pound Sterling",
              'KRW': "South Korean Won", 'MYR': "Malaysian Ringgit", 'EUR': "Euro"}
    REVERSE = {x[1].replace(' ', '').upper(): x[0] for x in VALUES.items()}

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
            print('Ошибка получения данных о курсе валют по сети!')
        # Явным образом добавляем базу рассчета
        self.cvalues['EUR'] = 1

    def get_price_cache(self, base: str, quote: str, amount: int) -> float:
        if (self.cache is None) or (datetime.datetime.now() - self.refresh > self.cache):
            self.refresh()
        # Ищем в UPPERCASE и без пробелов
        base = self.REVERSE.get(base.upper().replace(' ', ''), base.upper().replace(' ', ''))
        quote = self.REVERSE.get(quote.upper().replace(' ', ''), quote.upper().replace(' ', ''))
        if self.cvalues.get(base.upper(), None) is None:
            raise ApiException(f'Базовая валюта {base} отсутствует в списке доступных для конвертации!')
        if self.cvalues.get(quote.upper(), None) is None:
            raise ApiException(f'Результирующая валюта {quote} отсутствует в списке доступных для конвертации!')
        if amount <= 0:
            raise ApiException(f'Количество обмениваемой валюты должно быть целым положительным числом!')
        base = self.cvalues.get(base)
        quote = self.cvalues.get(quote)
        return amount / base * quote

    def values(self):
        result = ''
        for i in GetCurrency.VALUES.items():
            result += f'{i[0]}: {i[1]}\n'
        return result


class TgBot:
    # Чуть-чуть больше ООП богу ООП - но чуть-чуть меньше синтаксического сахара
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.set_update_listener(self.listner)
        self.changer = GetCurrency(cache=3600)
        self.bot.polling(none_stop=True)

    def listner(self, messages):
        for message in messages:
            if message.text.startswith('/help') or message.text.startswith('/start'):
                self.greet(message.chat.id)
            elif message.text.startswith('/convert'):
                try:
                    command = message.text.strip('/convert').split(',')
                    if len(command) != 3:
                        raise ApiException(
                            'Запрос на конвертацию принимает три параметра - исходную валюту, конечную и количество, разделенные запятыми')
                    else:
                        self.bot.send_message(message.chat.id,
                                              self.changer.get_price_cache(command[0], command[1],
                                                                           int(command[2])))
                except ApiException as err:
                    self.bot.reply_to(message, f'Ошибка пользователя! {err}\n')
                except Exception as err:
                    self.bot.reply_to(message, f'Не удалось обработать команду из-за ошибки {err}')
            elif message.text == '/values':
                self.bot.send_message(message.chat.id, self.changer.values())
            else:
                self.bot.reply_to(message,
                                  'Команда не распознана! Допустимые команды /help, /start /values /convert')

    def greet(self, id):
        self.bot.send_message(id, 'Здравствуйте. Вас приветствует конвертер валют. '
                                  'Для запроса курса валют воспользуйтесь командой /convert, '
                                  'для получения списка валют, в отношении которых возможна конвертация - /values')


if __name__ == '__main__':
    # Unit-тест на минималках
    exchange = GetCurrency(cache=None)
    print(exchange.get_price_cache('EUR', 'RUB', 100))
