#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random
import time

import numpy as np

import win32py


if __name__ == "__main__":
    t = time.time()
    while True:
        t1 = t
        image = win32py.screenshot()
        image = np.array(image)
        # ...
        t = time.time()
        print('screenshot: {}s'.format(t - t1))

        height, width, channel = image.shape
        w_center = width // 2
        h_center = height // 2

        win32py.Mouse.move(width // 2 + random.randint(-128, 128), height // 2 + random.randint(-96, 96))
        if random.random() > 0.5:
            win32py.Mouse.click(win32py.Mouse.Event.LEFT_DOWN)
            win32py.Mouse.click(win32py.Mouse.Event.LEFT_UP)
        key_prob = random.random()
        if key_prob < 0.25:
            win32py.Keyboard.click(win32py.Keyboard.Key.W)
        elif key_prob < 0.5:
            win32py.Keyboard.click(win32py.Keyboard.Key.A)
        elif key_prob < 0.75:
            win32py.Keyboard.click(win32py.Keyboard.Key.S)
        elif key_prob < 1.0:
            win32py.Keyboard.click(win32py.Keyboard.Key.D)
        print('total task: {}s'.format(time.time() - t1))
