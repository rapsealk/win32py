#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import ctypes
import PIL.ImageGrab

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
