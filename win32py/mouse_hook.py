#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import ctypes
from ctypes.wintypes import MSG
from multiprocessing import Queue
from threading import Thread

from util import get_function_pointer

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


# Mouse Logger
class MouseHook:

    def __init__(self, queue=None):
        self.hooked = None
        self.queue = queue or Queue()

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

    def run(self):
        msg = MSG()
        ctypes.windll.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0)

    def hook_procedure(self, nCode, wParam, lParam):    # LowLevelMouseProc
        if wParam == WM_LBUTTONDOWN:
            print('m_hook_procedure: LEFT')
            self.queue.put('LEFT')
        elif wParam == WM_RBUTTONDOWN:
            print('m_hook_procedure: RIGHT')
            print('Uninstall hook')
            self.uninstall_hook_procedure()
            sys.exit(-1)
        return ctypes.windll.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)


def digest_queue(queue):
    while True:
        item = queue.get()
        print('item:', item)


if __name__ == "__main__":
    queue = Queue()
    thread = Thread(target=digest_queue, args=(queue,), daemon=True)
    thread.start()

    mouse_hook = MouseHook(queue)
    pointer = get_function_pointer(mouse_hook.hook_procedure)
    if mouse_hook.install_hook_procedure(pointer):
        print('installed mouse_hook')
    mouse_hook.run()

    thread.join()
