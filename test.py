#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import unittest

import win32py


class Win32MouseTestCase(unittest.TestCase):

    def test_cursor_position(self):
        X, Y = (1024, 720)
        win32py.Mouse.move(X, Y)
        x, y = win32py.Mouse.get_cursor_pos()
        self.assertEqual((x, y), (X, Y))


if __name__ == "__main__":
    unittest.main()
