import sys
import sdl2
import sdl2.ext

WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)


class GPU:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pass
