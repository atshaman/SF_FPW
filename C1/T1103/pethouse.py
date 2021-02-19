#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов пользователей для услуги "Электронный кошелек" в рамках проекта "Дом питомца" упр. 1.10.3"""


class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    @property
    def name(self):
        return self._name.capitalize()

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.isalpha():
            self._name = value.lower()

    @property
    def surname(self):
        return self._surname.capitalize()

    @surname.setter
    def surname(self, value):
        if isinstance(value, str) and value.isalpha():
            self._surname = value.lower()


class Client(User):
    def __init__(self, name, surname, bill=0):
        User.__init__(self, name, surname)
        self.bill = bill

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        if isinstance(value, int) and value > 0:
            self._bill = value
        else:
            self._bill = 0

    def __str__(self):
        return f'Клиент {self.name} {self.surname}. Балланс {self._bill}'


class Clients:
    _clients = []

    def __init__(self, clients=None):
        if clients:
            self.clients = clients

    @property
    def clients(self):
        return '\n'.join([str(i) for i in self._clients])

    @clients.setter
    def clients(self, value):
        for i in value:
            if isinstance(i, Client):
                self._clients.append(i)

    def append(self, value):
        if isinstance(value, Client):
            self._clients.append(value)

    def extend(self, value):
        self._clients.extend(list(filter(lambda x: issubclass(type(x), User), value)))
