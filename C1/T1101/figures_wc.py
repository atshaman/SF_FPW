#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов геометрических фигур с возможностью задания координат
в рамках учебного задания 1.10.1"""
import math


class Rectangle:
    def __init__(self, width, height, x=1, y=1):
        self.width, self.height = width, height
        self.x, self.y = x, y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, int):
            self._x = value
        else:
            raise ValueError('Координата X должна быть целым числом!!')

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, int):
            self._y = value
        else:
            raise ValueError('Координата Y должна быть целым числом!!')

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if isinstance(value, int) and value > 0:
            self._width = value
        else:
            raise ValueError('Ширина должна быть целым положительным числом!')

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if isinstance(value, int) and value > 0:
            self._height = value
        else:
            raise ValueError('Высота должна быть целым положительным числом!')

    def get_area(self):
        return self._width * self._height

    def __str__(self):
        return '{}({}, {}, {}, {})'.format(self.__class__.__name__, self._x, self._y, self._width, self._height)


class Square(Rectangle):
    def __init__(self, side, x=1, y=1):
        Rectangle.__init__(self, side, side, x, y)

    def __str__(self):
        return '{}({}, {}, {})'.format(self.__class__.__name__, self._x, self._y, self._width)


class Circle(Square):
    def get_area(self):
        return self._width ** 2 * math.pi


if __name__ == '__main__':
    myfigures = [Rectangle(5, 10, x=10, y=20), Square(15), Circle(8)]
    for figure in myfigures:
        print(figure.get_area(), figure)
