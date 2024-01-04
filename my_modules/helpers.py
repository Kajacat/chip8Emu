import numpy as np


class Screen:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.screen = np.zeros((width, height), dtype=np.uint8)
        self.scale = scale
        self.sprite_row_size = 8
        self.sprite_column_size = 0
        self.sprite_row_start = 0
        self.sprite_column_start = 0

    def get_pixel(self, x, y):
        return self.screen[x, y]

    def set_pixel(self, x, y, value):
        self.screen[x, y] = value

    def clear(self):
        self.screen = np.zeros((self.width, self.height), dtype=np.uint8)


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)
