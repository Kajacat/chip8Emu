from my_modules.cpu import CPU


def run():
    # 1. load ROM into memory
    cpu = CPU()
    while True:
        cpu.run(0)
        # generate interrupts
        # emulate graphics
        # emulate sound
        # emulate other software components (e.g. gamepads, network etc.)
        # time synchronization


if __name__ == "__main__":
    run()
