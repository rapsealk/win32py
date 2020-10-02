#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import ctypes
import PIL.ImageGrab

# from . import windows
# from . import util
# from .keyboard_hook import KeyboardHook

if sys.platform != 'win32':
    import platform
    raise Exception('Invalid platform: %s (%s)' % (sys.platform, platform.platform()))


def screenshot():
    return PIL.ImageGrab.grab()


class Mouse:

    def __init__(self):
        pass

    @staticmethod
    def move(x, y, width=1280, height=720, x_offset=0, y_offset=0, is_relative=False):
        # ctypes.windll.user32.SetCursorPos(x, y)
        extra = ctypes.c_ulong(0)
        input_type = _InputType()
        dwFlags = Mouse.Event.MOVE
        if not is_relative:
            dwFlags |= Mouse.Event.ABSOLUTE
            x = 1 + int((x+x_offset) * 65536 / width)
            y = 1 + int((y+y_offset) * 65536 / height)
        input_type.mi = _MouseInput(x, y, 0, dwFlags, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), input_type)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    @staticmethod
    def move_on_foreground_window(x, y, width=1920, height=1080):
        #rect = get_foreground_window_rect()
        #Mouse.move(x+rect.left, y+rect.top, width=width, height=height)
        Mouse.move(x, y, width, height)

    @staticmethod
    def click(event):
        ctypes.windll.user32.mouse_event(event, 0, 0, 0, 0)

    @staticmethod
    def get_cursor_pos():
        point = _Point()
        if ctypes.windll.user32.GetCursorPos(ctypes.pointer(point)):
            return (point.x, point.y)
        else:
            return (0, 0)

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


class _Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong),
                ("y", ctypes.c_ulong)]


class _MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("pt", _Point),
                ("mouseData", ctypes.c_ulong),  # ctypes.wintypes.DWORD
                ("flags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


"""
class RAWINPUTDEVICE(ctypes.Structure):
    from ctypes.wintypes import HWND
    _fields_ = [("usUsagePage", ctypes.c_ushort),
                ("usUsage", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),    # == ctypes.wintypes.DWORD
                ("hwndTarget", HWND)]
"""


class Keyboard:

    class Key:
        N1 = 0x02
        Q = 0x10
        E = 0x12
        W = 0x11
        A = 0x1E
        S = 0x1F
        D = 0x20
        R = 0x13
        SHIFT = 0x2A
        SPACE = 0x39

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
    lib = ctypes.windll.user32
    handle = lib.GetForegroundWindow()
    buffer = ctypes.create_unicode_buffer(255)
    lib.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer))
    return buffer.value


class _Rect(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


def get_foreground_window_rect():
    lib = ctypes.windll.user32
    handle = lib.GetForegroundWindow()
    rect = _Rect()
    lib.GetWindowRect(handle, ctypes.pointer(rect))
    return rect


def get_foreground_window_grab():
    rect = get_foreground_window_rect()
    return PIL.ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
