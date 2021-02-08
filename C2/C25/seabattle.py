#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю C2"""
import random


class Point():
    _states = {0: '0', 1: '■', 2: 'X', 3: 'T'}

    def __init__(self, x=0, y=0, status=0):
        self.x = x
        self.y = y
        self.status = status

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
        if value > 0:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value > 0:
            self._y = value

    def __str__(self):
        return self._states[self._status]


class Ship():
    _points = []

    def __init__(self, x=0, y=0, rotation=0, size=1):
        self.rotation = rotation
        self.size = size
        for i in range(size):
            self._points.append(
                Point(x=x + (i if self.rotation else 0), y=y + (i if not self.rotation else 0), status=1))

    def near(self):
        return (self._points[0].x - 1, self._points[0].y - 1, self._points[-1].x + 1, self._points[-1].y + 1)

    def __contains__(self, item):
        pass

    def __str__(self):
        return ' '.join([str(x) for x in self._points])


class Field():
    _field = []  # Не нужно
    _sheeps = []
    _wounded = []

    def __init__(self, size=6):
        self._field = [[Point(x, y) for x in range(size)] for y in range(size)]

    def check(self):
        pass

    def draw(self):
        print('  0 1 2 3 4 5')
        for num, line in enumerate(self._field):
            print(num, ' '.join([str(x) for x in line]))


class Battle():
    def __init__(self):
        pass

    def fire(self):
        pass

    def run(self):
        while True:
            winner = self.turn()
            print(f'And the winner is... {winner}')


if __name__ == '__main__':
    t = Field()
    print(t.draw())
    """battle = Battle()
    battle.run()"""
