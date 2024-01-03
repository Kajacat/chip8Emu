import sdl2
import sdl2.ext

WHITE = 0xFFFFFF
BLACK = 0


class GPU:
    def __init__(self, screen, window_surface):
        self.screen = screen
        self.window_surface = window_surface

    def draw(self):
        sdl2.SDL_LockSurface(self.window_surface)

        pixels = sdl2.ext.pixels2d(self.window_surface)

        for y in range(self.screen.sprite_column_start*self.screen.scale,
                       (self.screen.sprite_column_start +
                        self.screen.sprite_column_size)*self.screen.scale):
            for x in range(self.screen.sprite_row_start*self.screen.scale,
                           (self.screen.sprite_row_start +
                            self.screen.sprite_row_size)*self.screen.scale):
                x_pixel = x // self.screen.scale
                y_pixel = y // self.screen.scale

                color = (WHITE
                         if self.screen.get_pixel(x_pixel, y_pixel)
                         else BLACK)

                pixels[x, y] = color

        sdl2.SDL_UnlockSurface(self.window_surface)
