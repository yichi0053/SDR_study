# Add in AWGN
import matplotlib.pyplot as plt
import numpy as np

num_symbols = 1000

x_int = np.random.randint(0, 4, num_symbols)
x_degrees = x_int * 360 / 4.0 + 45
x_radians = x_degrees * np.pi / 180.0
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)

# AWGN with unity power
n = (np.random.randn(num_symbols) + 1j * np.random.randn(num_symbols)) / np.sqrt(2)
noise_power = 0.01
r_awgn = x_symbols + n * np.sqrt(noise_power)

# phase noise
phase_noise = np.random.randn(num_symbols) * 0.1
r_phase = x_symbols * np.exp(1j * phase_noise)


fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].plot(np.real(r_awgn), np.imag(r_awgn), '.')
axes[0].set_title("AWGN")
axes[0].grid(True)

axes[1].plot(np.real(r_phase), np.imag(r_phase), '.')
axes[1].set_title("phase noise")
axes[1].grid(True)

plt.savefig("week1/d22_noise.png", dpi=120)
print("saved")