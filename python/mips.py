processor_frequency_hz = 3e9 # 3 Ghz - frequency == cycles per second
cycle_time_unit = 1 / processor_frequency_hz
instructions_per_cycle = 4 # assuming pipelining
instructions_per_second = instructions_per_cycle * processor_frequency_hz

# A 3 Ghz pipelined (4 inst/s) core is capable of 12,000 MIPS.
# If a single instruction access to memory (e.g., a fetch step in a load instruction)
# takes 70 nanoseconds. Then a 3 Ghz (3 billion cycles per second) processor would
# take ~23.3333333 cycles to execute that instruction's step.
