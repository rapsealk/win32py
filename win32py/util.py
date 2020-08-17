#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import ctypes


def first(func, iterable, optional=None):
    for item in iterable:
        if func(item):
            return item
    return optional


def get_function_pointer(fn):
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int,
                               ctypes.c_int,
                               ctypes.c_int,
                               ctypes.POINTER(ctypes.c_void_p))
    return CMPFUNC(fn)
