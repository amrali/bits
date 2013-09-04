"""\
A waves generation module
"""

from math import sin, pi
from itertools import izip, repeat
from collections import Iterable

def wave_gen(freq, amplitude=1, sample_rate=4.41e4):
    d = 0
    phase_delta = 2 * pi * freq / sample_rate
    while True:
        yield amplitude * sin(d)
        d += phase_delta

def frame_gen(samples=100, *wave_gens):
    waves = izip(*wave_gens)
    while samples > 0:
        yield sum(waves.next())
        samples -= 1

def waves(samples, freqs, amplitude=1, sample_rate=4.41e4):
    if not isinstance(amplitude, (int, long, float, Iterable)):
        raise RuntimeError("amplitude must be a number or an iterable")
    if not isinstance(freqs, Iterable):
        raise RuntimeError("freqs must be an iterable")
    if not isinstance(samples, (int, long)):
        raise RuntimeError("samples must be an integer")
    if not isinstance(amplitude, Iterable):
        amplitude = repeat(amplitude)

    wave_gens = []
    for freq, amp in izip(freqs, amplitude):
        wave_gens.append(wave_gen(freq, amp, sample_rate))
    return frame_gen(samples, *wave_gens)

