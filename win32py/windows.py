#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import ctypes


GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

titles = []


def foreach_window(hwnd, lparam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length+1)
        GetWindowText(hwnd, buff, length+1)
        titles.append(buff.value)
    return True


def get_window_titles():
    titles.clear()
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles.copy()
