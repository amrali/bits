import math
from collections import Counter

# http://rosettacode.org/wiki/Entropy#Python:_More_succinct_version
def H(data):
    if not data: return
    p, lns = Counter(data), float(len(data))
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

