#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

import win32py


if __name__ == "__main__":
    win32py.Mouse.move(300, 300)
    win32py.Mouse.click(win32py.Mouse.Event.RIGHT_DOWN)
    win32py.Mouse.click(win32py.Mouse.Event.RIGHT_UP)

    image = win32py.screenshot()
    # image.show()
    # image.save('filename.png')
    image = np.array(image)
    print(image.shape)
