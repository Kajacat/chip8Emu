import sdl2
import sdl2.ext
from my_modules.cpu import CPU
from my_modules.gpu import GPU
from my_modules.screen import Screen
import sys


def run(rom_path):
    # 1. load ROM into memory
    rom = []
    with open(rom_path, "rb") as f:
        byte = f.read(1)
        while byte:
            rom.append(format(ord(byte), "02x"))
            byte = f.read(1)
    # 2. initialize components
    screen = Screen(width=64, height=32)
    cpu = CPU(screen, rom)
    gpu = GPU(screen)
    # 3. run emulator
    while True:
        cpu.run()
        gpu.draw()
        # generate interrupts
        # emulate sound
        # emulate other software components (e.g. gamepads, network etc.)
        # time synchronization


if __name__ == "__main__":
    run(sys.argv[1])
