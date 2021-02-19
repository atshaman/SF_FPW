#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Работа с классами в рамках организации услуги "Электронный кошелек" в рамках проекта "Дом питомца" упр. 1.10.3"""
import pethouse

a = pethouse.Clients([pethouse.Client('Ivanov', 'Ivan', 100)])
a.append(pethouse.Client('Petrov', 'Petr'))
a.extend([pethouse.Client('Sidorov', 'Sergey'), 1, pethouse.Client('Zadov', 'Leonid')])
print(a.clients)
