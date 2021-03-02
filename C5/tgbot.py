# -*- coding: utf-8 -*-
"""Основная логика работы бота. Токен получаем из переменной окружения """

import extensions
import os

if __name__ == '__main__':
    token = os.environ.get('TOKEN', None)
    if token is None:
        raise extensions.ApiException('Отсутствует токен для запуска бота!')
    else:
        print('Bot are running...')
        bot = extensions.TgBot(token)
