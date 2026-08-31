# Verify that, after performing an FFT on a single-frequency signal,
# the spectral peak indeed appears at the correct frequency location.

import matplotlib.pyplot as plt
import numpy as np


def make_sine(f, fs, duration, amp=1.0, phase=0.0):
    n = np.arange(int(fs * duration))
    t = n / fs
    x = amp * np.sin(2 * np.pi * f * t + phase)
    return t, x


f = 50.0
fs = 1000.0
duration = 1.0

t, x = make_sine(f, fs, duration)
N = len(x)

X = np.fft.fft(x)   # Calculate "how strong each frequency component is" (the value on the vertical axis).
freqs = np.fft.fftfreq(N, d=1 / fs) # Calculate "which frequency corresponds to each position" (the scale on the horizontal axis).

X_shifted = np.fft.fftshift(X)
freqs_shifted = np.fft.fftshift(freqs)

magnitude = np.abs(X_shifted)   # Convert complex numbers to real-valued magnitude.

positive_mask = freqs_shifted >= 0  # Compare and return a True/False array
                                    # Used to filter the array and retain only the positive frequency component.
peak_idx = np.argmax(magnitude[positive_mask])
peak_freq = freqs_shifted[positive_mask][peak_idx]

print("N (sample size)    =", N)
print("frequency resolution (fs/N) =", fs / N, "Hz")
print("frequency          =", f, "Hz")
print("peak frequency     =", peak_freq, "Hz")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(freqs_shifted, magnitude)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("magnitude")
ax.set_title(f"FFT of {f} Hz sine wave (fs={fs} Hz)")
ax.grid(True)
fig.tight_layout()
fig.savefig("d03_fft_basic.png", dpi=120)
print("saved to d03_fft_basic.png")
