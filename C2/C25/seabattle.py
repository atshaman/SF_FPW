#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю C2"""
import random


class Point:
    # 0 - пусто, 1 - часть корабля, 2 - попадание, 3 - промах
    _states = {0: "0", 1: "■", 2: "X", 3: "T"}

    def __init__(self, x=0, y=0, status=0):
        self.x = x
        self.y = y
        self._status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in (0, 1, 2, 3):
            self._status = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value >= 0:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value >= 0:
            self._y = value

    def __eq__(self, other):
        try:
            if self._x == other[0] and self._y == other[1]:
                return True
            else:
                return False
        except:
            # Фу-фу-фу таким быть, но оно правда не равно
            return False

    def __str__(self):
        return self._states[self._status]


class Ship:

    def __init__(self, x=0, y=0, rotation=0, size=1):
        # 0 - корабль расположен горизонтально, 1 - вертикально
        self._points = []
        self.rotation = rotation
        self.size = size
        self._dead = False
        for i in range(size):
            self._points.append(
                Point(
                    x=x + (i if self.rotation else 0),
                    y=y + (i if not self.rotation else 0),
                    status=1,
                )
            )

    @property
    def dead(self):
        if all(self._points.status == 2):
            self._dead = True
            return True

    def near(self, point):
        # И снова фу-ф-фу, нечитаемо
        if (self._points[0].x - 1 <= point[0] <= self._points[-1].x + 1) and (
                self._points[0].y - 1 <= point[1] <= self._points[-1].y + 1
        ):
            return True
        else:
            return False

    def __contains__(self, item):
        # Можно через арифметику с х\у и обобщить с near, но "И так сойдет!"
        if item in self._points:
            return True
        else:
            return False

    def __str__(self):
        return " ".join([str(x) for x in self._points])


class Field:

    def __init__(self, size=6, ships={3: 1, 2: 2, 1: 4}, own=True):
        self.size = size
        self.own = own
        self._ships = []
        self._checked = []
        for i in sorted(ships.keys(), reverse=True):
            for j in range(ships[i]):
                self.setships(i)

    def setships(self, decks):
        print(decks)

    def check(self, point):
        # Проверяем координаты точки
        # Если поле наше (own) показываем корабли и проверенные поля. В противном случае только checked
        for i in self._ships:
            if point in i:
                return self._ships.index(i)
        return False

    def getfree(self):
        # Возвращаем множество свободных ячеек поля
        return set()

    def checkwin(self):
        # Проверяем не окончилась ли игра
        if all(self._ships.dead):
            return True
        else:
            return False

    def drawlines(self):
        yield "  " + " ".join([str(i) for i in range(self.size)])
        for y in range(self.size):
            result = str(y)
            for x in range(self.size):
                if not self.check((x, y)):
                    result += " 0"
                else:
                    result += f' {str(self._ships[self.check((x, y))])}'
            yield result


class Battle:
    def __init__(self, first=True, size=6, auto=False, fleet={3: 1, 2: 2, 1: 4}):
        self.first = first
        self.fleet = fleet
        self.size = size
        # Очередность хода. Левое поле всегда первое
        if auto:
            self._fields = (Field(self.size, self.fleet, True), Field(self.size, self.fleet, True))
        elif self.first:
            self._fields = (Field(self.size, self.fleet, True), Field(self.size, self.fleet, False))
        else:
            self._fields = (Field(self.size, self.fleet, False), Field(self.size, self.fleet, True))

    def shot(self, field):
        if self._fields[field].own:
            self._fields[field]._checked.append(random.choice(self._fields[field].getfree()))
        else:
            while True:
                coordinates = input('Введите координаты цели!')
                x, y = coordinates.split()
                if (int(x), int(y)) in self._fields[field].getfree:
                    self._fields[field]._checked.append(Point(x, y))
                    break
                else:
                    print('Точка занята')

    def round(self):
        # Поочередные ходы чет\нечет, после каждого хода проверяется условие победы и рисуется поле
        for i in self.size ** 2 * 2:
            self.draw()
            if i % 2:
                self.shot(0)
                if self._fields[0].checkwin():
                    return 0
            else:
                self.shot(1)
                if self._fields[1].checkwin():
                    return 1

    def draw(self):
        for i in zip(self._fields[0].drawlines(), self._fields[1].drawlines()):
            print(f'{i[0]}    |    {i[1]}')

    def run(self):
        while True:
            winner = self.round()
            print(f"And the winner is... {winner}")


if __name__ == "__main__":
    battle = Battle()
    battle.draw()
