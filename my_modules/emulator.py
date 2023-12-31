from my_modules.cpu import CPU
from my_modules.gpu import GPU
from my_modules.screen import Screen

def run():
    # 1. initialize components  
    screen = Screen(width = 64, height = 32)    
    cpu = CPU()
    gpu = GPU()
    
    # 2. load ROM into memory
    
    # 3. run emulator
    while True:
        cpu.run(0)
        # generate interrupts
        # emulate graphics
        # emulate sound
        # emulate other software components (e.g. gamepads, network etc.)
        # time synchronization


if __name__ == "__main__":
    run()
