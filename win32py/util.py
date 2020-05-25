#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


def first(func, iterable, optional=None):
    for item in iterable:
        if func(item):
            return item
    return optional
