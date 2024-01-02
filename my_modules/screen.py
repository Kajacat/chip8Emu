class Screen:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.screen = [0] * width * height
        self.scale = scale

    def get_pixel(self, x, y):
        return self.screen[y * self.width + x]

    def set_pixel(self, x, y, value):
        self.screen[y * self.width + x] = value

    def clear(self):
        self.screen = [0] * self.width * self.height
