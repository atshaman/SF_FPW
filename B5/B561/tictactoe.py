#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю B5"""
import random
import os
import os.path
import pickle


class Field:
    _values = {'0': 0, '1': 1, 'x': 1, 'o': 0, 0: 'o', 1: 'x'}

    def __init__(self, choice=None):
        self._field = [[None, None, None],
                       [None, None, None],
                       [None, None, None]]
        self._values['2'] = random.randint(0, 1)
        self.choice = choice

    def flash(self):
        """Сброс состояния """
        self.__init__(self)

    def draw(self):
        """Прорисовка поля с очисткой экрана """
        os.system('cls||clear')
        print('  0 1 2')
        for num, line in enumerate(self._field):
            print(num, ' '.join([self._values.get(x, '-') for x in line]))

    def chk_line(self):
        for i in self._field:
            for j in i:
                pass

    def mk_turn(self):
        """Ход компьютера """
        #Наивная реализация
        while True:
            x, y = random.randint(0,2), random.randint(0,2)
            if self.check_free(x, y):
                self._field[y][x] = 1 if not self.choice else 0
                break

    def get_turn(self):
        """Ход человека"""
        while True:
            try:
                x, y = input('Введите координаты следующего хода:\n').split()
                if self.check_free(int(x), int(y)):
                    self._field[int(y)][int(x)] = self.choice
                    break
            except IndexError:
                print('Необходимо ввести координаты x, y в диапазоне от 0 до 2!')
            except ValueError:
                print('Необходимо ввести две координаты!')

    def check_free(self, x, y):
        """Проверка свободы ячейки """
        if self._field[y][x] is None:
            return 1
        else:
            return 0

    def chk_condition(self):
        """Проверка условия победы """
        pass

    def getfirst(self):
        """Определение очередности хода """
        while True:
            try:
                self.choice = self._values[input(
                    'Выберите кто будет играть за X, 1 - игрок, 0 - компьюетер, 2 - случайный выбор:\n')]
                break
            except KeyError:
                print('Допустимые значения "0|o", "1|x", "2"')

    def run(self):
        """Главный цикл программы """
        while True:
            if not self.choice:
                self.getfirst()
            for i in range(9):
                if (i % 2 and not self.choice) or (not i % 2 and self.choice):
                    self.get_turn()
                else:
                    self.mk_turn()
                print(f'Ход номер {i}')
                self.draw()
            else:
                self.flash()
                self.choice = None

    def save(self):
        pass

    def load(self):
        pass


if __name__ == '__main__':
    field = Field()
    field.run()
