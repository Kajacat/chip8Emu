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
