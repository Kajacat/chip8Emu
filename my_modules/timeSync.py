# Timing: around 700MHz should work well
import time
import sdl2


class Timer:
    def __init__(self, hz=700):
        self.hz = hz

    def start(self):
        self.start_time = time.time()
        
    def wait(self):
        elapsed_time = time.time() - self.start_time
        time_to_wait = 1.0/self.hz - elapsed_time
        if time_to_wait > 0:
            sdl2.SDL_Delay(int(time_to_wait*1000))
        self.start_time = time.time()