from font import font
from collections import namedtuple
from functools import partial


OpcodeParts = namedtuple("OpcodeParts", ["F", "X", "Y", "N", "NN", "NNN"])


class CPU:
    def __init__(self):
        self.pc = 512  # Program Counter (start value in decimal)
        self.memory = [0] * 4096  # Memory with 4096 (bytes) locations
        self.stack = []  # Stack, 12 bits addresses
        self.registers = {
            "I": 0,  # Index register
            "Delay": 0,  # Delay timer, start at 60 and count down to 0, 60Hz
            "Sound": 0,  # Sound timer, start at 60 and count down to 0, 60Hz
        }

        # Merge font with memory
        self.memory[80 : 80 + len(font)] = font

    def fetch(self):
        opcode = (
            self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        )  # Instruction is 2 bytes long
        self.pc += 2

        F = opcode & 0xF000 >> 12
        X = opcode & 0x0F00 >> 8
        Y = opcode & 0x00F0 >> 4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF

        return OpcodeParts(F, X, Y, N, NN, NNN)

    def decode(self, opcode):
        if opcode.F == 0x0 and opcode.X == 0x0 and opcode.Y == 0xE and opcode.N == 0x0:
            return partial(self.clear_screen, opcode)

        raise NotImplementedError("Opcode not implemented")

    def execute(self, function):
        # This is a placeholder. You'll need to implement the actual opcode functions.
        pass

    def clear_screen(self, opcode):
        pass

    def jump(self):
        pass

    def set_register_VX(self):
        pass

    def add_register_VX(self):
        pass

    def set_register_I(self):
        pass

    def draw(self):
        pass

    decode_values = {
        "1": clear_screen,
        "2": jump,
        "3": set_register_VX,
        "4": add_register_VX,
        "5": set_register_I,
        "6": draw,
    }

    def decode_switch(self, case):
        return self.decode_values.get(case, "Invalid opcode")

    def run(self, cycles_to_execute):
        while executed_cycles < cycles_to_execute:
            opcode = self.fetch()
            function = self.decode(opcode)
            self.execute(function)


if __name__ == "__main__":
    cpu = CPU()
    cpu.run()
