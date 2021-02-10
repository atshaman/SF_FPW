#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов для итогового практического задания по модулю C2"""
import random


class Point:
    # 0 - пусто, 1 - промах, 3 - часть корабля, 4 - попадание
    # Сделаем аттрибутом класса
    _states = {0: "0", 3: "■", 4: "X", 1: "T"}

    def __init__(self, x=0, y=0, status=0):
        self.x = x
        self.y = y
        self.status = status

    def setstatus(self):
        self.status += 1
        try:
            return Point._states[self.status]
        except KeyError:
            self.status -= 1
            print('Фигня какая-то!')
            exit(-1)

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
        return Point._states[self.status]


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
                    status=3,
                )
            )

    @property
    def dead(self):
        if not self.dead and all([x.status == 4 for x in self._points]):
            self._dead = True
        return self._dead

    def near(self):
        # Возвращаем множество точек рядом
        # И снова фу-ф-фу, нечитаемо
        return set([(x, y) for x in range(self._points[0].x - 1, self._points[-1].x + 2) for y in
                    range(self._points[0].y - 1, self._points[-1].y + 2)])

    def __contains__(self, item):
        # Можно через арифметику с х\у и обобщить с near, но "И так сойдет!"
        if item in self._points:
            return True
        else:
            return False

    def getpoint(self, x, y):
        for i in self._points:
            if i == (x, y):
                return str(i)

    def coordinates(self):
        return [(p.x, p.y) for p in self._points]

    def __str__(self):
        return " ".join([str(x) for x in self._points])


class Field:

    def __init__(self, size=6, ships={3: 1, 2: 2, 1: 4}, own=True):
        self.size = size
        # Own - принадлежит человеку
        self.own = own
        self._ships = []
        self._checked = []
        for i in sorted(ships.keys(), reverse=True):
            for j in range(ships[i]):
                self._ships.append(self.setships(i))
                if self.own == 1:
                    for k in self.drawlines(): print(k)

    def setships(self, decks):
        free = self.getfree()
        while True:
            try:
                # Не надо так - слишком большой облок обернут
                if self.own != 1:
                    ship = Ship(*random.choice(free), random.randint(0, 1), decks)
                else:
                    print(f'Введите координаты левой верхней точки {decks}-клеточного корабля')
                    x, y = self.getcoordinates()
                    if decks != 1:
                        orientatiton = input('Укажите ориентацию корабля: 0 - горизонтально, 1 - вертикально')
                    else:
                        orientatiton = decks
                    if int(orientatiton) not in (0, 1):
                        raise Exception('Положение корабля может быть горизонтальным (0) или вертикальным (1)!')
                    ship = Ship(x, y, random.randint(0, 1), decks)
                if all([x in free for x in ship.coordinates()]):
                    return ship
                else:
                    raise Exception('Корабли не могут соприкасаться друг с другом!')
            except Exception as err:
                # И так тоже не надо. Слишком общее исключение заметено под ковер.
                if self.own == 1:
                    print(err)

    def check(self, point):
        # Проверяем координаты точки
        # Если поле наше (own) показываем корабли и проверенные поля. В противном случае только checked
        for i in self._ships:
            if self.own in (1, 2) and point in i:
                return self._ships.index(i)
        if point in self._checked:
            return self._checked.index(point)
        return None

    def getfree(self):
        # Возвращаем множество свободных ячеек поля
        result = set([(x, y) for x in range(self.size) for y in range(self.size)])
        bisy = set([(p.x, p.y) for p in self._checked])
        for i in self._ships:
            bisy.update(i.near())
        return list(result.difference(bisy))

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
                if self.check((x, y)) is None:
                    result += " 0"
                else:
                    result += f' {self._ships[self.check((x, y))].getpoint(x, y)}'
            yield result

    def getcoordinates(self):
        while True:
            coordinates = input('Введите координаты!')
            try:
                x, y = coordinates.split()
                if not (0 <= int(x) <= self.size or 0 <= int(y) <= self.size):
                    raise Exception(f'Координаты не могут выходить за пределы поля - 0, {self.size}')
                if (int(x), int(y)) not in self._checked:
                    return (int(x), int(y))
                else:
                    print('Точка занята')
            except ValueError:
                print('Координаты задаются в виде двух чисел, разделенных пробелом')
            except Exception as err:
                # И опять фу-фу-фу, слишком общее исключение
                print(err)


class Battle:
    def __init__(self, first=1, size=7, fleet={3: 1, 2: 2, 1: 4}):
        self.first = first
        self.fleet = fleet
        self.size = size
        # Очередность хода. Левое поле всегда первое
        if self.first == 2:
            self._fields = (Field(self.size, self.fleet, 2), Field(self.size, self.fleet, 2))
        elif self.first == 1:
            self._fields = (Field(self.size, self.fleet, 1), Field(self.size, self.fleet, 0))
        else:
            self._fields = (Field(self.size, self.fleet, 0), Field(self.size, self.fleet, 1))

    def shot(self, field):
        if not self._fields[field].own:
            self._fields[field]._checked.append(random.choice(self._fields[field].getfree()))
        else:
            x, y = self._fields[field].getcoordinates()

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
    battle = Battle(first=2)
    battle.draw()
