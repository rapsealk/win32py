#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import time

import numpy as np

import win32py


if __name__ == "__main__":
    # win32py.Mouse.move(300, 300)
    # win32py.Mouse.click(win32py.Mouse.Event.RIGHT_DOWN)
    # win32py.Mouse.click(win32py.Mouse.Event.RIGHT_UP)

    image = win32py.screenshot()
    # image.show()
    # image.save('filename.png')
    image = np.array(image)
    print(image.shape)

    print(win32py.get_foreground_window_title())

    # for i in range(108):
    #     win32py.Keyboard.press(0x00 + i)
    #     win32py.Keyboard.release(0x00 + i)

    # win32py.Keyboard.press(win32py.Keyboard.Key.N1)
    # win32py.Keyboard.release(win32py.Keyboard.Key.N1)
    # win32py.Keyboard.click(win32py.Keyboard.Key.W)
    # win32py.Keyboard.click(win32py.Keyboard.Key.A)
    # win32py.Keyboard.click(win32py.Keyboard.Key.S)
    # win32py.Keyboard.click(win32py.Keyboard.Key.D)
