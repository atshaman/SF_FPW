#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю B5"""
import random
import os
import collections


class Field:
    _values = {'0': 0, '1': 1, 'x': 1, 'o': 0, 0: 'x', 1: '0'}

    def __init__(self, choice=None, mode=1, scroll=False):
        self._field = [None for i in range(9)]
        self._values['2'] = random.randint(0, 1)
        self.mode = mode
        self.choice = choice
        self.scroll = scroll

    def greet(self):
        print(
            'Доброе пожаловать в игру крестики-нолики. Игра запускается в следующих режимах: 1 - игра с комьютером, 0 - hot-seat, 3 - автотест')

    def draw(self):
        """Прорисовка поля с очисткой экрана """
        if not self.scroll:
            os.system('cls||clear')
        print('  0 1 2')
        for num, line in enumerate([self._field[i * 3:i * 3 + 3] for i in range(len(self._field) // 3)]):
            print(num, ' '.join([self._values.get(x, '-') for x in line]))

    def mk_turn(self, turn):
        """Ход компьютера """
        # Чуть менее наивная реализация, позволяет обойтись без проверки занятости клетки
        if self._field[4] is None:
            self._field[4] = turn % 2
        else:
            self._field[
                random.choice([x for x, y in enumerate(self._field) if y is None])] = turn % 2

    def get_turn(self, turn):
        """Ход человека, поддерживается ввод с пробелом и без"""
        while True:
            try:
                index = input(
                    "Введите координаты следующего хода (Допускаются координаты в форматах 'xy', 'x y', 'N' - номер ячейки):\n")
                if len(index) == 1:
                    index = int(index)
                elif len(index) == 2:
                    index = int(index[0]) + int(index[1]) * 3
                else:
                    index = int(index.replace(' ', '')[0]) + int(index.replace(' ', '')[1]) * 3
                if self._field[index] is None:
                    self._field[index] = turn % 2
                    break
                else:
                    print(f"Клетка {index - (index // 3 * 3)}:{index // 3} занята!")
            except ValueError:
                print('Необходимо ввести координаты x, y в диапазоне от 0 до 2!')

    def chk_condition(self):
        """Проверка условия победы """
        # Оптимальным в данном случае была бы последовательная проверка всех прямых в матрице
        # Диагонали
        scores = [self._field[::4], self._field[2:7:2]]
        # Вертикали+горизонтали
        for i in range(len(self._field) // 3):
            scores.append(self._field[i * 3:i * 3 + 3])
            scores.append(self._field[i::3])
        for score in map(collections.Counter, scores):
            if score[1] == 3:
                return 1
            elif score[0] == 3:
                return 0
        return None

    def getfirst(self):
        """Определение очередности хода """
        while True:
            try:
                self.choice = self._values[input(
                    'Выберите кто будет играть за X, 1|x - игрок, 0|o - компьютер, 2 - случайный выбор:\n')]
                break
            except KeyError:
                print('Допустимые значения "0|o", "1|x", "2"')

    def round(self):
        for i in range(9):
            print(f'Ход номер {i}')
            if (i % 2 and not self.choice) or (not i % 2 and self.choice):
                if self.mode != 3:
                    self.get_turn(i)
                else:
                    self.mk_turn(i)
            else:
                self.mk_turn(i)
            self.draw()
            if self.chk_condition() is not None:
                print(f'На {i} ходу победили {self._values[self.chk_condition()]}')
                break
        else:
            print("Ничья!")

    def run(self):
        """Главный цикл программы """
        while True:
            if not self.choice:
                self.getfirst()
            self.draw()
            self.round()
            self.__init__(self, mode=self.mode, scroll=self.scroll)


if __name__ == '__main__':
    field = Field(mode=0)
    field.run()
