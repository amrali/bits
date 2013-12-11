import math
from collections import Counter

def H(data):
    if not data: return

    entropy = 0
    data_len = float(len(data))
    data_freq = dict(Counter(data)) # Any zero elements are not included
    p_x = [data_freq[chr(x)] / data_len for x in range(256) if chr(x) in data_freq]
    return reduce(lambda x, y: x + (- y * math.log(y, 2)), p_x, 0)

