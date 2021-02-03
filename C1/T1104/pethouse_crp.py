#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов пользователей для проведения корпоратива в рамках проекта "Дом питомца" упр. 1.10.4"""


class Address(dict):
    def __init__(self, city=None, street=None, house=None):
        dict.__init__(self)
        self['city'] = city
        self['street'] = street
        self['house'] = house

    def __str__(self):
        return f"Город {self['city']}, улица {self['street']}, дом {self['house']}"


class User:
    def __init__(self, name, surname, address):
        self.name = name
        self.surname = surname
        if isinstance(address, Address):
            self.address = address
        else:
            raise ValueError('Адрес должен быть объектом класса Address!')

    @property
    def name(self):
        return self._name.capitalize()

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.isalpha():
            self._name = value.lower()
        else:
            raise ValueError('Имя должно быть строкой!')

    @property
    def surname(self):
        return self._surname.capitalize()

    @surname.setter
    def surname(self, value):
        if isinstance(value, str) and value.isalpha():
            self._surname = value.lower()
        else:
            raise ValueError('Фамилия должно быть строкой!')


class Client(User):
    def __init__(self, name, surname, address, bill=0):
        User.__init__(self, name, surname, address)
        self.bill = bill

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        try:
            if int(value) > 0:
                self._bill = value
            else:
                self._bill = 0
        except ValueError:
            print('Значение на счете должно быть целым положительным числом!')
            exit(-1)

    def __str__(self):
        return f'Клиент {self.name} {self.surname}. Адрес - {self.address}. Балланс {self._bill}'


class Employee(User):
    _states = {'наставник': 0, 'н': 0, 'работник': 1, 'р': 1}

    def __init__(self, name, surname, address, status):
        User.__init__(self, name, surname, address)
        try:
            self.state = self._states[status.lower()]
        except KeyError:
            print(f"Работник может быть в следующем статусе: {'|'.join(self._states.keys())}")
            exit(-1)

    def __str__(self):
        return f'Работник {self.name} {self.surname}. Адрес - {self.address}. Статус {"Работник" if self.state else "Наставник"}'


class People:
    _people = []

    def __init__(self, people=None):
        if people:
            self.people = people

    @property
    def people(self):
        return '\n'.join([str(i) for i in self._people])

    @people.setter
    def people(self, value):
        for i in value:
            if issubclass(type(i), User):
                self._people.append(i)

    def append(self, value):
        if issubclass(type(value), User):
            self._people.append(value)

    def extend(self, value):
        self._people.extend(list(filter(lambda x: issubclass(type(x), User), value)))


if __name__ == '__main__':
    a = People([Client('Ivanov', 'Ivan', Address('1', '2', '3'), 100)])
    a.append(Client('Petrov', 'Petr', Address('4', '5', '6')))
    a.extend([Client('Sidorov', 'Sergey', Address('1', '2', '3')), 1,
              Employee('Zadov', 'Leonid', Address('1', '2', '3'), 'н')])
    print(a.people)
