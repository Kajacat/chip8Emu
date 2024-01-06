import sdl2
import sdl2.ext
import numpy as np
import ctypes


class Sound:
    def __init__(self):
        # Parameters for the beep sound
        frequency = 440  # Frequency in Hz
        sample_rate = 44100  # Sample rate in Hz
        duration = 1  # Duration in seconds

        # Generate a sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        beep = np.sin(frequency * t * 2 * np.pi)

        # Ensure that highest value is in 16-bit range
        audio = (beep * 32767 / np.max(np.abs(beep))).astype(np.int16)

        # Convert to bytes
        self.audio_bytes = audio.tobytes()

        # Create an SDL audio buffer
        self.audio_buffer = sdl2.SDL_malloc(len(self.audio_bytes))
        ctypes.memmove(self.audio_buffer, self.audio_bytes, len(self.audio_bytes))

        # Create an SDL audio specification
        audio_spec = sdl2.SDL_AudioSpec(freq=sample_rate, aformat=sdl2.AUDIO_S16LSB, channels=1, samples=4096)

        # Open the audio device
        print(sdl2.SDL_GetNumAudioDevices(0))
        print(sdl2.SDL_GetAudioDeviceName(0, 0))
        
        self.audio_device = sdl2.SDL_OpenAudioDevice(None, 0, audio_spec, None, 0)

    def play_sound(self):
        # Queue the audio data and start playing
        sdl2.SDL_QueueAudio(self.audio_device, self.audio_buffer, len(self.audio_bytes))
        sdl2.SDL_PauseAudioDevice(self.audio_device, 0)

    def stop_sound(self):
        # Stop playing
        sdl2.SDL_PauseAudioDevice(self.audio_device, 1)
        
    def cleanup(self):
        sdl2.SDL_CloseAudioDevice(self.audio_device)
        sdl2.SDL_free(self.audio_buffer)