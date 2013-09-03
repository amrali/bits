"""
A wave generator module
"""

from math import sin, pi
from itertools import izip

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
