import sdl2
import sdl2.ext
from cpu import CPU
from gpu import GPU
from screen import Screen
from keyboard import Keyboard
import sys


def run(rom_path):
    # 1. load ROM into memory
    rom = []
    with open(rom_path, "rb") as f:
        byte = f.read(1)
        while byte:
            rom.append(int.from_bytes(byte, byteorder="big"))
            byte = f.read(1)

    # 2. initialize components
    screen = Screen(width=64, height=32, scale=10)
    keyboard = Keyboard()

    sdl2.ext.init()
    window = sdl2.ext.Window("Chip 8 emulator",
                             size=(screen.width*screen.scale,
                                   screen.height*screen.scale))
    window_surface = window.get_surface()

    cpu = CPU(screen, rom, keyboard)
    gpu = GPU(screen, window_surface)

    window.show()

    # 3. run emulator
    running = True
    while running:
        events = sdl2.ext.get_events()
        cpu.run()
        gpu.draw()
        window.refresh()

        # generate interrupts
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                mapped_key = keyboard.map_sdl_key(event.key.keysym.sym)
                if mapped_key is not None:
                    keyboard.set_pressed(mapped_key)
            elif event.type == sdl2.SDL_KEYUP:
                mapped_key = keyboard.map_sdl_key(event.key.keysym.sym)
                if mapped_key is not None:
                    keyboard.set_released(mapped_key)

        # emulate sound
        # time synchronization

    # 4. clean up
    sdl2.ext.quit()


if __name__ == "__main__":
    run(sys.argv[1])
