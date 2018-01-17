from random import randint
from hashlib import sha1 # per hashcash docs it does use the 160-bit SHA-1 hash

counter = 1#randint(1, int(1e6)) # an arbitrary range
salt = randint(1, 256)
header_template = lambda x: 'This is an example header: {} {}'.format(salt, x).encode('utf8')

def first_x_bits(val, bits=20):
    size = len(val) * 8 # in bits
    if size < bits:
        return

    int_val = int.from_bytes(val, 'big', signed=False)
    return int_val >> size - bits

bits = 20
h_val = lambda: sha1(header_template(counter))
while first_x_bits(h_val().digest(), bits) != 0:
    counter += 1

print(h_val().hexdigest(), counter)

counter +=1

while first_x_bits(h_val().digest(), bits) != 0:
    counter += 1

print(h_val().hexdigest(), counter)
