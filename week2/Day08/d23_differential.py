# Differential encoding and decoding
import numpy as np

bits = np.array([1, 1, 0, 0, 1, 1, 1, 1, 1, 0])

# encode: y[i] = y[i-1] XOR x[i]
encoded = np.zeros(len(bits) + 1, dtype=int)
encoded[0] = 1  # arbitrary staring bit
for i in range(len(bits)):
    encoded[i+1] = encoded[i] ^ bits[i]

# decode: x[i] = y[i] XOR y[i-1]
def decode(y):
    return y[1:] ^ y[:-1]

decoded = decode(encoded)

# simulate 180 degree phase flip (all bits inverted)
flipped = 1 - encoded
decoded_flipped = decode(flipped)

print("original: ", bits)
print("encoded:  ", encoded)
print("decoded:  ", decoded)
print("flipped:  ", flipped)
print("decoded after flip:", decoded_flipped)