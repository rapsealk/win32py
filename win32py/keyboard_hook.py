#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import ctypes
from ctypes.wintypes import MSG
from multiprocessing import Queue
from threading import Thread

from .util import get_function_pointer

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
    def __init__(self, queue=None, digest_fn=None):
        global key_hook

        key_hook = self

        self.hooked = None
        self.queue = queue or Queue()

        self.thread = None
        if digest_fn and callable(digest_fn):
            self.thread = Thread(target=digest_fn, args=(self.queue,), daemon=True)  # noqa: E501
            self.thread.start()

    def __del__(self):
        print('KeyboardHook.__del__')
        if self.thread:
            self.thread.join()

    def install_hook_procedure(self, pointer, dwThreadId=0):
        module_handle = ctypes.windll.kernel32.GetModuleHandleW(None)
        self.hooked = ctypes.windll.user32.SetWindowsHookExA(WH_KEYBOARD_LL,
                                                             pointer,
                                                             module_handle,
                                                             dwThreadId)
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


def hook_procedure(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return ctypes.windll.user32.CallNextHookEx(key_hook.hooked,
                                                   nCode,
                                                   wParam,
                                                   lParam)
    lparam = (lParam[0] >> 32)  # and 0xFFFF

    if CTRL_CODE == int(lparam):
        print("Ctrl pressed, call uninstallHook()")
        key_hook.uninstall_hook_procedure()
        sys.exit(-1)

    try:
        hooked_key = KEY_MAP[int(lparam)]
    except KeyError:
        return ctypes.windll.user32.CallNextHookEx(key_hook.hooked,
                                                   nCode,
                                                   wParam,
                                                   lParam)
    key_hook.queue.put((int(time.time() * 1000), hooked_key))
    return ctypes.windll.user32.CallNextHookEx(key_hook.hooked,
                                               nCode,
                                               wParam,
                                               lParam)


def digest_queue(queue):
    while True:
        item = queue.get()
        print('item:', item)


def main():
    # global key_hook

    queue = Queue()
    key_hook = KeyboardHook(queue, digest_fn=digest_queue)
    pointer = get_function_pointer(hook_procedure)
    if key_hook.install_hook_procedure(pointer):
        print("installed keyLogger")
    key_hook.run()


if __name__ == "__main__":
    main()
