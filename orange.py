import wave
from pyb import DAC
def play_wave(file):
    dac = DAC(1)
    f = wave.open(file)
    dac.write_timed(f.readframes(f.getnframes()), f.getframerate())
