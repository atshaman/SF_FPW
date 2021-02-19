#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Работа с классоми геометрических фигур в рамках задания 1.9.1 """
import figures

myfigures = [figures.Rectangle(5, 10), figures.Square(15), figures.Circle(8)]
for figure in myfigures:
    print(figure.get_area())
