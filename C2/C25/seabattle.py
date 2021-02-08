#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю C2"""
import random


class Point:
    _states = {0: "0", 1: "■", 2: "X", 3: "T"}

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
    _points = []

    def __init__(self, x=0, y=0, rotation=0, size=1):
        # 0 - корабль расположен горизонтально, 1 - вертикально
        self.rotation = rotation
        self.size = size
        for i in range(size):
            self._points.append(
                Point(
                    x=x + (i if self.rotation else 0),
                    y=y + (i if not self.rotation else 0),
                    status=1,
                )
            )

    def near(self, point):
        # И снова фу-ф-фу, нечитаемо
        if (self._points[0].x - 1 <= point[0] <= self._points[-1].x + 1) and (
            self._points[0].y - 1 <= point[1] <= self._points[-1].y + 1
        ):
            return True
        else:
            return False

    def __contains__(self, item):
        # Можно через арифметику с х\у и обобщить с near, но пока "И так сойдет!"
        if item in self._points:
            return True
        else:
            return False

    def __str__(self):
        return " ".join([str(x) for x in self._points])


class Field:
    _field = []  # Не нужно
    _ships = [Ship(0, 0, 0, 3)]
    _checked = []

    def __init__(self, size=6, ships={}, own=True):
        self.size = size
        self.own = own

    def getships(self):
        pass

    def setships(self):
        pass

    def check(self, point):
        for i in self._ships:
            if point in i:
                return self._ships.index(i)
        return False

    def drawlines(self):
        yield "  " + " ".join([i for i in range(self.size)])
        for y in range(self.size):
            result = " "
            for x in range(self.size):
                if not self.check(x, y):
                    result += " 0 "
            yield result


class Battle:
    def __init__(self):
        pass

    def getfire(self):
        pass

    def setfire(self):
        pass

    def run(self):
        while True:
            winner = self.turn()
            print(f"And the winner is... {winner}")


if __name__ == "__main__":
    # t = Field()
    # print(t.draw())
    test = Ship(2, 2, 1, 3)
    print(test.near((5, 4)))
    """battle = Battle()
    battle.run()"""
