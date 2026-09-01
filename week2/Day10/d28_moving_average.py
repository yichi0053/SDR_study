import matplotlib.pyplot as plt
import numpy as np

fs = 1000.0
t = np.arange(1000) / fs

# clean low frequency signal + noise
signal = np.sin(2 * np.pi * 5 * t)
noisy = signal + 0.5 * np.random.randn(len(t))

# moving average filter, all-ones taps
h = np.ones(20) / 20

filtered = np.convolve(noisy, h, mode='same')   # mode="same" makes len(input) = len(output)

fig, axes = plt.subplots(2, 1, figsize=(10, 6))

axes[0].plot(t, noisy, label="noisy")
axes[0].plot(t, filtered, label="filtered")
axes[0].legend()
axes[0].set_title("moving average smooths out noise")

freqs = np.fft.fftshift(np.fft.fftfreq(len(t), d=1/fs))
H = np.abs(np.fft.fftshift(np.fft.fft(h, len(t))))
axes[1].plot(freqs, H)
axes[1].set_xlim(0, 100)
axes[1].set_xlabel("frequency (Hz)")
axes[1].set_title("frequency response of moving average filter")

plt.tight_layout()
plt.savefig("d28_moving_average.png", dpi=120)
print("saved")