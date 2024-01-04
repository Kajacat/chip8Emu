import sdl2


class Keyboard:
    def __init__(self):
        self.keys = {
            0x0: 0,  # 1
            0x1: 0,  # 2
            0x2: 0,  # 3
            0x3: 0,  # 4
            0x4: 0,  # Q
            0x5: 0,  # W
            0x6: 0,  # E
            0x7: 0,  # R
            0x8: 0,  # A
            0x9: 0,  # S
            0xA: 0,  # D
            0xB: 0,  # F
            0xC: 0,  # Z
            0xD: 0,  # X
            0xE: 0,  # C
            0xF: 0,  # V
        }
        self.keymap = {
            sdl2.SDLK_1: 0x0,
            sdl2.SDLK_2: 0x1,
            sdl2.SDLK_3: 0x2,
            sdl2.SDLK_4: 0x3,
            sdl2.SDLK_q: 0x4,
            sdl2.SDLK_w: 0x5,
            sdl2.SDLK_e: 0x6,
            sdl2.SDLK_r: 0x7,
            sdl2.SDLK_a: 0x8,
            sdl2.SDLK_s: 0x9,
            sdl2.SDLK_d: 0xA,
            sdl2.SDLK_f: 0xB,
            sdl2.SDLK_z: 0xC,
            sdl2.SDLK_x: 0xD,
            sdl2.SDLK_c: 0xE,
            sdl2.SDLK_v: 0xF,
            }

    def is_pressed(self, key):
        if key in self.keys:
            return self.keys[key]

    def set_pressed(self, key):
        if key in self.keys:
            self.keys[key] = 1

    def set_released(self, key):
        if key in self.keys:
            self.keys[key] = 0

    def map_sdl_key(self, key):
        if key in self.keymap:
            return self.keymap[key]
        else:
            return None

    def get_pressed_key_if_any(self):
        for key in self.keys:
            if self.keys[key] == 1:
                return key
        return None
