#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import ctypes
import PIL.ImageGrab

import win32py.windows

if sys.platform != 'win32':
    import platform
    raise Exception('Invalid platform: %s (%s)' % (sys.platform, platform.platform()))


def screenshot():
    return PIL.ImageGrab.grab()


class Mouse:

    def __init__(self):
        pass

    @staticmethod
    def move(x, y):
        ctypes.windll.user32.SetCursorPos(x, y)

    @staticmethod
    def click(event):
        ctypes.windll.user32.mouse_event(event, 0, 0, 0, 0)

    class Event:
        """
        https://docs.microsoft.com/ko-kr/windows/win32/api/winuser/nf-winuser-mouse_event
        """
        ABSOLUTE = 0x8000
        LEFT_DOWN = 0x0002
        LEFT_UP = 0x0004
        MIDDLE_DOWN = 0x0020
        MIDDLE_UP = 0x0040
        MOVE = 0x0001
        RIGHT_DOWN = 0x0008
        RIGHT_UP = 0x0010
        WHEEL = 0x0800
        X_DOWN = 0x0080
        X_UP = 0x0100


class _KeyboardInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class _HardwardInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class _MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class _InputType(ctypes.Union):
    _fields_ = [("ki", _KeyboardInput),
                ("mi", _MouseInput),
                ("hi", _HardwardInput)]


class _Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", _InputType)]


class Keyboard:

    class Key:
        N1 = 0x02
        W = 0x11
        A = 0x1E
        S = 0x1F
        D = 0x20

    @staticmethod
    def click(key_code):
        Keyboard.press(key_code)
        Keyboard.release(key_code)

    @staticmethod
    def press(key_code):
        extra = ctypes.c_ulong(0)
        input_type = _InputType()
        input_type.ki = _KeyboardInput(0, key_code, 0x0008, 0, ctypes.pointer(extra))
        key = _Input(ctypes.c_ulong(1), input_type)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(key), ctypes.sizeof(key))

    @staticmethod
    def release(key_code):
        extra = ctypes.c_ulong(0)
        input_type = _InputType()
        input_type.ki = _KeyboardInput(0, key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        key = _Input(ctypes.c_ulong(1), input_type)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(key), ctypes.sizeof(key))


def get_foreground_window_title():
    titles = windows.get_window_titles()
    try:
        return titles[1]
    except IndexError:
        return titles[0]
