#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Работа с классами для проведения корпоратива в рамках проекта "Дом питомца" упр. 1.10.4"""
import pethouse_crp

participants = pethouse_crp.People()

greeting = '''Подготовка к проведению корпоратива Pethouse. Для прохождения вам необходимо зарегистрировать участников
0 - выход из системы
1 - работа в пакетном режиме
2 - работа в интерактивном режиме
3 - печать списка участников
4 - помощь'''

print(greeting)
print('-' * 50)
while True:
    value = input('Ждем...\n')
    if value == '0':
        break
    elif value == '1':
        # Batch mode
        value = input('Введите участников мероприятия в формате Фамилия Имя Город Улица Дом Счет\n')
        value = value.split()
        if not len(value) % 6:
            for i in range(len(value) // 6):
                slice = value[i * 6:i * 6 + 6]
                print(slice)
                participants.append(pethouse_crp.Client(*slice[0:2], pethouse_crp.Address(*slice[2:5]), slice[-1]))
        else:
            print(f'Ошибка! Число параметров ({len(value)}) не соответствует требуемому!')
    elif value == '2':
        pass
    elif value == '3':
        print(participants.people)
    elif value == '4':
        print(greeting)
        print('-' * 50)
    else:
        print('Введите одно из допустимых значиний: 0, 1, 2, 3, 4')
