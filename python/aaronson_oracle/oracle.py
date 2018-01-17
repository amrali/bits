import sys

from collections import defaultdict, deque
from functools import partial

# n-gram probabilistic model
model = defaultdict(partial(dict, f=0, d=0))

def window(seq, n):
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield win
    for e in it:
        win.append(e)
        yield win

def predict_letter(five_gram):
    m = model[five_gram]

    if (m['f'] > m['d']):
        return 'f'

    return 'd'

def predict(S):
    for last_six in window(S, 6):
        last = last_six.pop()
        fivegram = ''.join(list(last_six))

        # predict next value
        prediction = predict_letter(fivegram)

        # update model
        model[fivegram][last] += 1

        yield [prediction, last]

while True:
    line = sys.stdin.readline()
    if not line:
        break

    line = line[:-1]
    for p, r in predict(line):
        print(p, r)
