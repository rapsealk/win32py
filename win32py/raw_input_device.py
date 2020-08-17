#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import ctypes

"""
# Mouse movement: https://docs.microsoft.com/en-us/windows/win32/dxtecharts/taking-advantage-of-high-dpi-mouse-movement
HID_USAGE_PAGE_GENERIC = 0x01
HID_USAGE_GENERIC_MOUSE = 0x02

RIDEV_REMOVE        = 0x00000001
RIDEV_EXCLUDE       = 0x00000010
RIDEV_PAGEONLY      = 0x00000020
RIDEV_NOLEGACY      = 0x00000030
RIDEV_INPUTSINK     = 0x00000100
RIDEV_CAPTUREMOUSE  = 0x00000200
RIDEV_NOHOTKEYS     = 0x00000200
RIDEV_APPKEYS       = 0x00000400
RIDEV_EXINPUTSINK   = 0x00001000
RIDEV_DEVNOTIFY     = 0x00002000

WM_INPUT = 0x00FF
WM_MOUSEMOVE = 0x0200
"""

"""
def register_rawinputdevice():
    rid = RAWINPUTDEVICE()
    rid.usUsagePoge = HID_USAGE_PAGE_GENERIC
    rid.usUsage = HID_USAGE_GENERIC_MOUSE
    rid.dwFlags = RIDEV_NOHOTKEYS   # RIDEV_INPUTSINK
    rid.hwndTarget = None   # ctypes.wintypes.HWND()
    return ctypes.windll.user32.RegisterRawInputDevices(ctypes.pointer(rid), 1, ctypes.sizeof(RAWINPUTDEVICE))


def m_hook_procedure_raw(nCode, wParam, lParam):
    if wParam == WM_INPUT:
        print('m_hook_procedure_raw:', wParam, lParam)
    return ctypes.windll.user32.CallNextHookEx(True, nCode, wParam, lParam)
"""

if __name__ == "__main__":
    # if not register_rawinputdevice():
    #     print('Failed to register RawInputDevice!')
    #     sys.exit(-1)
    # pointer = get_function_pointer(m_hook_procedure_raw)
