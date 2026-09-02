import matplotlib.pyplot as plt
import numpy as np

# --- create a test IQ file (pretend this came from someone else) ---
num_symbols = 5000
x_int = np.random.randint(0, 4, num_symbols)
x_radians = (x_int * 360 / 4.0 + 45) * np.pi / 180.0
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)
n = (np.random.randn(num_symbols) + 1j * np.random.randn(num_symbols)) / np.sqrt(2)
r = (x_symbols + n * np.sqrt(0.01)).astype(np.complex64)
r.tofile('test.iq')

# --- now pretend we received this file with no prior knowledge ---
samples = np.fromfile('test.iq', np.complex64)

print("number of samples:", len(samples))
print("dtype:", samples.dtype)
print("max |sample|:", np.max(np.abs(samples)))
print("min real:", np.min(samples.real), " max real:", np.max(samples.real))

plt.plot(np.real(samples), np.imag(samples), '.')
plt.grid(True)
plt.title("constellation of loaded IQ file")
plt.savefig("d31_load_iq.png", dpi=120)
print("saved")