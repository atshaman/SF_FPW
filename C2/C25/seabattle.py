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
        # 0 - жив, 1 - ранен, 2 - убит
        self._status = 0
        for i in range(size):
            self._points.append(
                Point(
                    x=x + (i if self.rotation else 0),
                    y=y + (i if not self.rotation else 0),
                    status=3,
                )
            )

    @property
    def status(self):
        if self._status == 2:
            return self._status
        if all([x.status == 4 for x in self._points]):
            self._status = 2
            print(f'Корабль с координатами {self.coordinates()} уничтожен!')
        else:
            if any([x.status == 4 for x in self._points]):
                self._status = 1
        return self._status

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

    def setpoint(self, x, y):
        for i in self._points:
            if i == (x, y):
                i.setstatus()
                return i

    def coordinates(self):
        return [(p.x, p.y) for p in self._points]

    def __str__(self):
        return " ".join([str(x) for x in self._points])


class Field:

    def __init__(self, size=6, ships={3: 1, 2: 2, 1: 4}, own=2, fleet=None):
        self.size = size
        # Own - принадлежит человеку, 1 - да, 2 автобой, 0 - компьютер
        self.own = own
        self._ships = []
        self._checked = []
        if not fleet:
            for i in sorted(ships.keys(), reverse=True):
                for j in range(ships[i]):
                    self._ships.append(self.setships(i))
                    if self.own == 1:
                        for k in self.drawlines(): print(k)
        else:
            self._ships += fleet

    def setships(self, decks):
        free = self.getfree()
        while True:
            try:
                # Не надо так - слишком большой облок обернут
                if self.own != 1:
                    ship = Ship(*random.choice(free), random.randint(0, 1), decks)
                else:
                    print(f'Введите координаты левой верхней точки {decks}-клеточного корабля\n')
                    x, y = self.getcoordinates()
                    if decks != 1:
                        orientatiton = input('Укажите ориентацию корабля: 0 - горизонтально, 1 - вертикально\n')
                    else:
                        orientatiton = decks
                    if int(orientatiton) not in (0, 1):
                        raise Exception('Положение корабля может быть горизонтальным (0) или вертикальным (1)!')
                    ship = Ship(x, y, orientatiton, decks)
                if all([x in free for x in ship.coordinates()]):
                    return ship
                else:
                    raise Exception('Корабли не могут соприкасаться друг с другом!')
            except Exception as err:
                # И так тоже не надо. Слишком общее исключение заметено под ковер.
                if self.own == 1:
                    print(err)

    def check(self, point):
        # Проверяем координаты точки, возвращаем None или индекс точки в корабле
        for i in self._ships:
            if point in i:
                return self._ships.index(i)
        return None

    def getfree(self):
        # Возвращаем множество свободных ячеек поля
        result = set([(x, y) for x in range(self.size) for y in range(self.size)])
        # Два раза в одно место стрелять нельзя никому
        busy = set([(p.x, p.y) for p in self._checked])
        for i in self._ships:
            # Первоначальная расстановка
            if len(self._checked) == 0:
                busy.update(i.near())
            # Если поле принадлежит компьютеру - не стреляем около убитых кораблей. Игрок имет право быть идиотом.
            elif i.status == 2 and self.own != 1:
                busy.update(i.near())
        return list(result.difference(busy))

    def checkwin(self):
        # Проверяем не окончилась ли игра
        if all([x.status == 2 for x in self._ships]):
            return True
        else:
            return False

    def drawlines(self):
        yield "  " + " ".join([str(i) for i in range(self.size)])
        for y in range(self.size):
            result = str(y)
            for x in range(self.size):
                elem = " 0"
                if self.check((x, y)) is None:
                    if (x, y) in self._checked:
                        elem = " T"
                else:
                    if self.own in (1, 2):
                        elem = f' {self._ships[self.check((x, y))].getpoint(x, y)}'
                    else:
                        if (x, y) in self._checked:
                            elem = f' {self._ships[self.check((x, y))].getpoint(x, y)}'
                result += elem
            yield result

    def getcoordinates(self):
        while True:
            coordinates = input('Введите координаты!\n')
            try:
                x, y = coordinates.split()
                if not (0 <= int(x) <= self.size or 0 <= int(y) <= self.size):
                    raise Exception(f'Координаты не могут выходить за пределы поля - 0, {self.size}\n')
                if (int(x), int(y)) not in self._checked:
                    return (int(x), int(y))
                else:
                    print('Точка занята')
            except ValueError:
                print('Координаты задаются в виде двух чисел, разделенных пробелом\n')
            except Exception as err:
                # И опять фу-фу-фу, слишком общее исключение
                print(err)


class Battle:
    def __init__(self, first=1, size=7, ships={3: 1, 2: 2, 1: 4}, fleet=None):
        self.first = first
        self.ships = ships
        self.size = size
        # Очередность хода. Левое поле всегда первое
        if self.first == 2:
            self._fields = (Field(self.size, self.ships, 2), Field(self.size, self.ships, 2))
        elif self.first == 1:
            self._fields = (Field(self.size, self.ships, 1, fleet), Field(self.size, self.ships, 0))
        else:
            self._fields = (Field(self.size, self.ships, 0), Field(self.size, self.ships, 1, fleet))

    def shot(self, field):
        if self._fields[field].own in (1, 2):
            # Тут бы нарисовать вместо свирепого рандома что-нибудь более приличное для раненых кораблей, но времени нет
            x, y = random.choice(self._fields[field].getfree())
        else:
            while True:
                x, y = self._fields[field].getcoordinates()
                if (x, y) in self._fields[field]._checked:
                    print('Нельзя дважды стрелять в одно место!\n')
                else:
                    break
        if self._fields[field].check((x, y)) is not None:
            self._fields[field]._checked.append(
                self._fields[field]._ships[self._fields[field].check((x, y))].setpoint(x, y))
        else:
            self._fields[field]._checked.append(Point(x, y, 1))
        print(f'Выстрел по координатам {x},{y}\n')

    def round(self):
        # Поочередные ходы чет\нечет, после проверки условий победы делается выстрел и рисуется поле
        self.draw()
        for i in range(self.size ** 2 * 2):
            self.shot(i % 2)
            if self._fields[i % 2].checkwin():
                return i % 2
            print(f'Ход номер {i}\n')
            self.draw()

    def draw(self):
        print(
            f'{"Комьютер" if self._fields[0].own != 1 else "Человек"}               {"Комьютер" if self._fields[1].own != 1 else "Человек"}')
        for i in zip(self._fields[0].drawlines(), self._fields[1].drawlines()):
            print(f'{i[0]}    |    {i[1]}')

    def run(self):
        while True:
            winner = self.round()
            print(f"And the winner is... {winner}")
            exit = input('Нажмите любую кнопку для продолжения, 0 для выхода\n')
            if exit == '0':
                break
            else:
                self.__init__(first=self.first, size=self.size, ships=self.ships)


if __name__ == "__main__":
    battle = Battle(first=2, fleet=[Ship(0, 0, 1, 3), Ship(2, 2, 0, 2), Ship(3, 4, 1, 2), Ship(0, 2, 0), Ship(0, 4, 0),
                                    Ship(0, 6, 0), Ship(6, 6, 0)])
    battle.run()
