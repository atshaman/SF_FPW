#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Работа с классами для проведения корпоратива в рамках проекта "Дом питомца" упр. 1.10.4"""
import pethouse_crp

participants = pethouse_crp.People()

greeting = '''Подготовка к проведению корпоратива PETHOUSE. Для прохождения вам необходимо зарегистрировать участников
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
        value = input('Введите участников мероприятия в формате Фамилия Имя Город Улица Дом Счет\n').split()
        if not len(value) % 6:
            for i in range(len(value) // 6):
                slice = value[i * 6:i * 6 + 6]
                if slice[-1].isnumeric():
                    participants.append(pethouse_crp.Client(*slice[0:2], pethouse_crp.Address(*slice[2:5]), slice[-1]))
                elif slice[-1].isalpha():
                    participants.append(
                        pethouse_crp.Employee(*slice[0:2], pethouse_crp.Address(*slice[2:5]), slice[-1]))
        else:
            print(f'Ошибка! Число параметров ({len(value)}) не соответствует требуемому!')
    elif value == '2':
        name = input('Введите имя:\n')
        surname = input("Введите фамилию:\n")
        city = input("Введите город:\n")
        street = input("Введите улицу:\n")
        house = input("Введите дом:\n")
        address = pethouse_crp.Address(city, street, house)
        user_type = input('Укажите тип лица к - клиент, р - работник:')
        while True:
            if user_type == 'к':
                bill = input('Укажите сумму на счете:\n')
                participants.append(pethouse_crp.Client(name, surname, address, bill))
                break
            elif user_type == 'р':
                worker_type = input('Укажите тип работника наставник - "н" или работник "р":\n')
                participants.append(pethouse_crp.Employee(name, surname, address, worker_type))
                break
            else:
                print('Лицо может быть клиентом (к) или работником (р)!')
    elif value == '3':
        print(participants.people)
    elif value == '4':
        print(greeting)
        print('-' * 50)
    else:
        print('Введите одно из допустимых значиний: 0, 1, 2, 3, 4')
