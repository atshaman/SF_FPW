#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю B5"""
import random
import os


class Field:
    _values = {'0': 1, 1: 'X', 'o': 1, '1': -1, 'x': -1, -1: '0'}

    def __init__(self, choice=None, mode=1, scroll=False):
        # 0 обозначается -1, Х - единицей
        self._field = [0]*9
        self._values['2'] = random.randint(0, 1)
        self.mode = mode
        self.choice = choice
        self.scroll = scroll

    @staticmethod
    def greet():
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
        if self._field[4] == 0:
            self._field[4] = self._values[str(turn % 2)]
        else:
            self._field[
                random.choice([x for x, y in enumerate(self._field) if y == 0])] = self._values[str(turn % 2)]

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
                if self._field[index] == 0:
                    self._field[index] = self._values[str(turn % 2)]
                    break
                else:
                    print(f"Клетка {index - (index // 3 * 3)}:{index // 3} занята!")
            except ValueError:
                print('Необходимо ввести координаты x, y в диапазоне от 0 до 2!')
            except IndexError:
                print('Размеры поля ограничены 3*3!')

    def score(self):
        """По умолчанию score каждой клетки - 0. За принадлежность к пустой линии - +=1
        Если в линии есть еще один 'наш' элемент - +2, если в линии есть наш и не наш - линия =0 """
        pass

    def chk_condition(self):
        """Проверка условия победы """
        # Оптимальным в данном случае была бы последовательная проверка всех прямых в матрице
        # Диагонали
        scores = [sum(self._field[::4]), sum(self._field[2:7:2])]
        # Вертикали+горизонтали
        for i in range(len(self._field) // 3):
            scores.append(sum(self._field[i * 3:i * 3 + 3]))
            scores.append(sum(self._field[i::3]))
        if any([x == -3 for x in scores]):
            return -1
        elif any([x == 3 for x in scores]):
            return 1
        return None

    def getfirst(self):
        """Определение очередности хода """
        while True:
            try:
                choice = input(
                    'Выберите кто будет играть за X, 1|x - игрок, 0|o - компьютер, 2 - случайный выбор, 3 - автоигра, Q|q - выход:\n')
                if choice.lower() == '3':
                    self.choice = 1
                    self.mode = 3
                elif choice.lower() == 'q':
                    exit(0)
                else:
                    self.choice = self._values[choice]
                    self.mode = 0
                break
            except KeyError:
                print('Допустимые значения "0|o", "1|x", "2"')

    def round(self):
        for i in range(9):
            print(f'Ход номер {i}')
            if (i % 2 and self.choice == 1) or (not i % 2 and self.choice == -1):
                if self.mode != 3:
                    self.get_turn(i)
                else:
                    self.mk_turn(i)
            else:
                self.mk_turn(i)
            print(self._field)
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
            Field.__init__(self, mode=self.mode, scroll=self.scroll)


if __name__ == '__main__':
    field = Field(mode=3, scroll=True)
    field.run()
