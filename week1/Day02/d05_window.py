# Compare the degree of spectral leakage before and after windowing 
# to understand the practical effect of windowing.

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann


def make_sine(f, fs, duration, amp=1.0, phase=0.0):
    n = np.arange(int(fs * duration))
    t = n / fs
    x = amp * np.sin(2 * np.pi * f * t + phase)
    return t, x


f = 50.0
fs = 1000.0
duration = 0.213

t, x = make_sine(f, fs, duration)
N = len(x)

freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))

X_rect = np.fft.fftshift(np.fft.fft(x)) # "rectangular" windowing
mag_rect_db = 20 * np.log10(np.abs(X_rect) + 1e-12) # Add a very small value to ensure the logarithm of zero is not taken.
                                                    # "20 * log10" -> Standard formula for converting to dB.

window = hann(N)
x_windowed = x * window
X_hann = np.fft.fftshift(np.fft.fft(x_windowed))
mag_hann_db = 20 * np.log10(np.abs(X_hann) + 1e-12)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(freqs, mag_rect_db, label="no window (rectangular)", alpha=0.8) # spectral leakage (recall Convolution in Frequency Property)
ax.plot(freqs, mag_hann_db, label="Hann window", alpha=0.8)
ax.set_xlim(-200, 200)
ax.set_ylim(-60, 40)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("magnitude (dB)")
ax.set_title(f"spectral leakage comparison (duration={duration}s, N={N})")
ax.legend()
ax.grid(True)

fig.tight_layout()
fig.savefig("d05_window.png", dpi=120)
print("saved to d05_window.png")
print("N =", N, ", duration*f =", duration * f, "(Non-integer values ​​represent non-integer periods.)")