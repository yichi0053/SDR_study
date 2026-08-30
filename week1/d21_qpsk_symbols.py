import matplotlib.pyplot as plt
import numpy as np

num_symbols= 1000

x_int = np.random.randint(0, 4, num_symbols)

# map to 45, 135, 225, 315 degrees
x_degrees = x_int * 360 / 4.0 + 45
x_radians = x_degrees * np.pi / 180.0

x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)

plt.plot(np.real(x_symbols), np.imag(x_symbols), '.')
plt.grid(True)
plt.xlabel("I")
plt.ylabel("Q")
plt.title("QPSK constellation")
plt.savefig("week1/d21_qpsk_symbols.png", dpi=120)
print("saved")