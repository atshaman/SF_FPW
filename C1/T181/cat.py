#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание класса Cat в рамках учебного задания 1.8.1"""


class Cat():
    _genders = {'male': 0, 'm': 0, 'мужской': 0, 'м': 0, 'female': 1, 'f': 1, 'женский': 1, 'ж': 1}

    def __init__(self, gender, age, name):
        self.gender = gender
        self.age = age
        self.name = name

    @property
    def gender(self):
        if self._gender == 0:
            return 'мужской'
        else:
            return 'женский'

    @gender.setter
    def gender(self, value):
        try:
            self._gender = self._genders[value.lower()]
        except KeyError:
            print('Пол должен быть одним из: ' + '/'.join(list(self._genders.keys())))

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if int(value) > 0 and int(value) < 100:
            self._age = value
        else:
            raise ValueError('Возраст должен быть целым положительным числом в диапазоне от 0 до 100')

    @property
    def name(self):
        return self._name.capitalize()

    @name.setter
    def name(self, value):
        if value.isalpha() and len(value) < 20:
            self._name = value.lower()
        else:
            raise ValueError('Имя должно быть текстовой строкой до длинной до 20 символов')

    def get_info(self):
        return ('Питомец {0}, возраст {1}, пол {2}'.format(self.name, self.age, self.gender))
