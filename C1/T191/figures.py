#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Описание классов геометрических фигур в рамках учебного задания 1.9.1"""
import math


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

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


class Square(Rectangle):
    def __init__(self, side):
        self.width = self.height = side


class Circle(Square):

    def get_area(self):
        return self._width ** 2 * math.pi
