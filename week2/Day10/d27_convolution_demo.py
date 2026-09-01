import matplotlib.pyplot as plt
import numpy as np

f = np.array([0, 0, 1, 1, 1, 0, 0])
g = np.array([0, 0, 1, 1, 1, 0, 0])

output = np.convolve(f, g)

print("f length:", len(f))
print(f)
print("g length:", len(g))
print(g)
print("output length:", len(output))
print("expected N+M-1:", len(f) + len(g) - 1)
print(output)

plt.plot(output, '.-')
plt.title("convolution of two square pulses")
plt.savefig("d27_convolution_demo.png", dpi=120)
print("saved")