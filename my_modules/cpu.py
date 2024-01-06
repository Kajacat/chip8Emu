from font import font
from collections import namedtuple
from functools import partial
from collections import deque
import numpy as np

OpcodeParts = namedtuple("OpcodeParts", ["F", "X", "Y", "N", "NN", "NNN"])


class CPU:
    def __init__(self, screen, rom, keyboard):
        self.pc = 512  # Program Counter (start value in decimal)
        self.memory = [0x0] * 4096  # Memory with 4096 (bytes) locations
        self.stack = deque()  # Stack, 12 bits addresses
        self.registers = {
            "I": 0,  # Index register
            "Delay": 63,  # Delay timer, 60Hz
            "Sound": 63,  # Sound timer, 60Hz
            "V": [0] * 16,  # 16 8-bit registers
        }

        # Merge font with memory
        self.font_start = 80
        self.memory[self.font_start: self.font_start + len(font)] = font
        self.memory[self.pc: self.pc + len(rom)] = rom
        self.screen = screen
        self.keyboard = keyboard

    def fetch(self):
        opcode = (
            (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        )  # Instruction is 2 bytes long
        self.pc += 2

        F = (opcode & 0xF000) >> 12
        X = (opcode & 0x0F00) >> 8
        Y = (opcode & 0x00F0) >> 4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF

        return OpcodeParts(F, X, Y, N, NN, NNN)

    def decode(self, opcode):
        if (opcode.F == 0x0 and
                opcode.X == 0x0 and
                opcode.Y == 0xE and
                opcode.N == 0x0):
            return partial(self.clear_screen, opcode)

        if (opcode.F == 0x1):
            return partial(self.jump, opcode)

        if (opcode.F == 0x0 and
                opcode.X == 0x0 and
                opcode.NN == 0xEE):
            return partial(self.subroutines_pop, opcode)

        if (opcode.F == 0x2):
            return partial(self.subroutines_push, opcode)

        if (opcode.F == 0x3):
            return partial(self.skip_single_equal, opcode)

        if (opcode.F == 0x4):
            return partial(self.skip_single_unequal, opcode)

        if (opcode.F == 0x5):
            return partial(self.skip_multi_equal, opcode)

        if (opcode.F == 0x6):
            return partial(self.set_register_VX, opcode)

        if (opcode.F == 0x7):
            return partial(self.add_register_VX, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x0):
            return partial(self.copy_register, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x1):
            return partial(self.bitwise_or, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x2):
            return partial(self.bitwise_and, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x3):
            return partial(self.bitwise_xor, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x4):
            return partial(self.add_register_VY, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x5):
            return partial(self.subtract_register_VY, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x6):
            return partial(self.shift_right, opcode)

        if (opcode.F == 0x8 and opcode.N == 0xE):
            return partial(self.shift_left, opcode)

        if (opcode.F == 0x8 and opcode.N == 0x7):
            return partial(self.subtract_register_VX, opcode)

        if (opcode.F == 0x9):
            return partial(self.skip_multi_unequal, opcode)

        if (opcode.F == 0xA):
            return partial(self.set_register_I, opcode)

        if (opcode.F == 0xB):
            return partial(self.jump_offset, opcode)

        if (opcode.F == 0xC):
            return partial(self.random, opcode)

        if (opcode.F == 0xD):
            return partial(self.draw, opcode)

        if (opcode.F == 0xE and opcode.NN == 0x9E):
            return partial(self.skip_key_equal, opcode)

        if (opcode.F == 0xE and opcode.NN == 0xA1):
            return partial(self.skip_key_unequal, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x07):
            return partial(self.delay_timer_get, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x15):
            return partial(self.delay_timer_set, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x18):
            return partial(self.sound_timer_set, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x1E):
            return partial(self.add_register_I, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x0A):
            return partial(self.key_wait, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x29):
            return partial(self.set_register_I_to_font, opcode)
        
        if (opcode.F == 0xF and opcode.NN == 0x33):
            return partial(self.bcd_conversion, opcode)

        if (opcode.F == 0xF and opcode.NN == 0x55):
            return partial(self.store_registers, opcode)
        
        if (opcode.F == 0xF and opcode.NN == 0x65):
            return partial(self.load_registers, opcode)
        
        raise NotImplementedError("Opcode not implemented")

    def run(self):
        self.registers["Delay"] = max(0, self.registers["Delay"] - 1)
        self.registers["Sound"] = max(0, self.registers["Sound"] - 1)
        opcode = self.fetch()
        function = self.decode(opcode)
        self.execute(function)

    def execute(self, function):
        function()

    def clear_screen(self, opcode):
        self.screen.clear()

    def jump(self, opcode):
        self.pc = opcode.NNN

    def subroutines_push(self, opcode):
        self.stack.append(self.pc)
        self.pc = opcode.NNN

    def subroutines_pop(self, opcode):
        self.pc = self.stack.pop()

    def skip_single_equal(self, opcode):
        if self.registers["V"][opcode.X] == opcode.NN:
            self.pc += 2

    def skip_single_unequal(self, opcode):
        if self.registers["V"][opcode.X] != opcode.NN:
            self.pc += 2

    def skip_multi_equal(self, opcode):
        if self.registers["V"][opcode.X] == self.registers["V"][opcode.Y]:
            self.pc += 2

    def skip_multi_unequal(self, opcode):
        if self.registers["V"][opcode.X] != self.registers["V"][opcode.Y]:
            self.pc += 2

    def set_register_VX(self, opcode):
        self.registers["V"][opcode.X] = opcode.NN

    def add_register_VX(self, opcode):
        self.registers["V"][opcode.X] += opcode.NN

    def copy_register(self, opcode):
        self.registers["V"][opcode.X] = self.registers["V"][opcode.Y]

    def bitwise_or(self, opcode):
        self.registers["V"][opcode.X] |= self.registers["V"][opcode.Y]

    def bitwise_and(self, opcode):
        self.registers["V"][opcode.X] &= self.registers["V"][opcode.Y]

    def bitwise_xor(self, opcode):
        self.registers["V"][opcode.X] ^= self.registers["V"][opcode.Y]

    def add_register_VY(self, opcode):
        self.registers["V"][opcode.X] += self.registers["V"][opcode.Y]
        self.registers["V"][0xF] = (1 if self.registers["V"][opcode.X] > 255
                                    else 0)

    def subtract_register_VY(self, opcode):
        self.registers["V"][opcode.X] -= self.registers["V"][opcode.Y]
        self.registers["V"][0xF] = (1 if self.registers["V"][opcode.X] > 0
                                    else 0)

    def subtract_register_VX(self, opcode):
        self.registers["V"][opcode.X] = (self.registers["V"][opcode.Y] -
                                         self.registers["V"][opcode.X])
        self.registers["V"][0xF] = (1 if self.registers["V"][opcode.X] > 0
                                    else 0)

    def shift_right(self, opcode):
        # possibly set VX to VY first
        self.registers["V"][0xF] = self.registers["V"][opcode.X] & 0x1
        self.registers["V"][opcode.X] >>= 1

    def shift_left(self, opcode):
        # possibly set VX to VY first
        self.registers["V"][0xF] = (self.registers["V"][opcode.X] >> 7) & 0x1
        self.registers["V"][opcode.X] <<= 1

    def set_register_I(self, opcode):
        self.registers["I"] = opcode.NNN

    def jump_offset(self, opcode):
        # possibly jump to XNN + V_X
        self.pc = opcode.NNN + self.registers["V"][0x0]

    def random(self, opcode):
        self.registers["V"][opcode.X] = np.random.randint(0, 255) & opcode.NN

    def draw(self, opcode):
        # Draw a sprite at position VX, VY with N bytes of sprite data
        # starting at the address stored in I
        sprite_data = self.memory[self.registers["I"]:
                                  self.registers["I"] + opcode.N]
        x_start = self.registers["V"][opcode.X] & (self.screen.width - 1)
        y_start = self.registers["V"][opcode.Y] & (self.screen.height - 1)
        self.registers["V"][0xF] = 0

        x = x_start
        y = y_start

        self.screen.sprite_column_size = opcode.N
        self.screen.sprite_row_start = x_start
        self.screen.sprite_column_start = y_start

        for sprite_row in sprite_data:
            for pixel_index in range(8):
                x = x_start + (7 - pixel_index)

                if x >= self.screen.width:
                    continue

                pixel = sprite_row >> pixel_index & 0x1
                current_pixel = self.screen.get_pixel(x, y)
                new_pixel = current_pixel ^ pixel
                self.registers["V"][0xF] |= current_pixel & pixel & 0x1
                self.screen.set_pixel(x, y, new_pixel)
            y += 1

    def skip_key_equal(self, opcode):
        if self.keyboard.is_pressed(self.registers["V"][opcode.X]):
            self.pc += 2

    def skip_key_unequal(self, opcode):
        if not self.keyboard.is_pressed(self.registers["V"][opcode.X]):
            self.pc += 2

    def delay_timer_get(self, opcode):
        self.registers["V"][opcode.X] = self.registers["Delay"]

    def delay_timer_set(self, opcode):
        self.registers["Delay"] = self.registers["V"][opcode.X]

    def sound_timer_set(self, opcode):
        self.registers["Sound"] = self.registers["V"][opcode.X]

    def add_register_I(self, opcode):
        self.registers["I"] += self.registers["V"][opcode.X]
        if self.registers["I"] > 0xFFF:
            self.registers["V"][0xF] = 1

    def key_wait(self, opcode):
        pressed_key = self.keyboard.get_pressed_key_if_any()
        if pressed_key is not None:
            self.registers["V"][opcode.X] = pressed_key
            # possibly only continue if pressed key is released
        else:
            self.pc -= 2

    def set_register_I_to_font(self, opcode):
        font_length = 5
        self.registers["I"] = ((self.registers["V"][opcode.X] & 0x0F) * font_length
                               + self.font_start)

    def bcd_conversion(self, opcode):
        self.memory[self.registers["I"]] = self.registers["V"][opcode.X] // 100
        self.memory[self.registers["I"] + 1] = (self.registers["V"][opcode.X] // 10) % 10
        self.memory[self.registers["I"] + 2] = self.registers["V"][opcode.X] % 10
    
    def store_registers(self, opcode):
        # possibly increment I for older games
        for i in range(opcode.X + 1):
            self.memory[self.registers["I"] + i] = self.registers["V"][i]
    
    def load_registers(self, opcode):
        # possibly increment I for older games
        for i in range(opcode.X + 1):
            self.registers["V"][i] = self.memory[self.registers["I"] + i]