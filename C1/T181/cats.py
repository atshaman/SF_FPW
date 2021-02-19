#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Работа с классом Cat в рамках задания 1.8.1 """

import cat

cats = [cat.Cat('m', 2, 'сэм'), cat.Cat('m', 2, 'барон')]
for i in cats:
    print(i.get_info())
