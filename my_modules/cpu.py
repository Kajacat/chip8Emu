from font import font
from collections import namedtuple
from functools import partial


OpcodeParts = namedtuple("OpcodeParts", ["F", "X", "Y", "N", "NN", "NNN"])


class CPU:
    def __init__(self, screen, rom):
        self.pc = 512  # Program Counter (start value in decimal)
        self.memory = [0x0] * 4096  # Memory with 4096 (bytes) locations
        self.stack = []  # Stack, 12 bits addresses
        self.registers = {
            "I": 0,  # Index register
            "Delay": 0,  # Delay timer, start at 60 and count down to 0, 60Hz
            "Sound": 0,  # Sound timer, start at 60 and count down to 0, 60Hz
            "V": [0] * 16,  # 16 8-bit registers
        }

        # Merge font with memory
        self.memory[80: 80 + len(font)] = font
        self.memory[self.pc: self.pc + len(rom)] = rom
        self.screen = screen

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

        if (opcode.F == 0x6):
            return partial(self.set_register_VX, opcode)

        if (opcode.F == 0x7):
            return partial(self.add_register_VX, opcode)

        if (opcode.F == 0xA):
            return partial(self.set_register_I, opcode)

        if (opcode.F == 0xD):
            return partial(self.draw, opcode)

        raise NotImplementedError("Opcode not implemented")

    def run(self):
        opcode = self.fetch()
        function = self.decode(opcode)
        self.execute(function)

    def execute(self, function):
        function()

    def clear_screen(self, opcode):
        self.screen.clear()

    def jump(self, opcode):
        self.pc = opcode.NNN

    def set_register_VX(self, opcode):
        self.registers["V"][opcode.X] = opcode.NN

    def add_register_VX(self, opcode):
        self.registers["V"][opcode.X] += opcode.NN

    def set_register_I(self, opcode):
        self.registers["I"] = opcode.NNN

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
