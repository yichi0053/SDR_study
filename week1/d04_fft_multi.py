# Verify that superimposed multi-frequency signals can be clearly separated in the frequency domain,
# yet no discernible structure is visible in the time-domain plot.

import matplotlib.pyplot as plt
import numpy as np


def make_sine(f, fs, duration, amp=1.0, phase=0.0):
    n = np.arange(int(fs * duration))
    t = n / fs
    x = amp * np.sin(2 * np.pi * f * t + phase)
    return t, x


fs = 1000.0
duration = 1.0

f1, amp1 = 50.0, 1.0
f2, amp2 = 120.0, 0.5
f3, amp3 = 300.0, 0.3

t, x1 = make_sine(f1, fs, duration, amp=amp1)
_, x2 = make_sine(f2, fs, duration, amp=amp2)   # "_" -> The return value is not needed, intentionally discard.
_, x3 = make_sine(f3, fs, duration, amp=amp3)

x = x1 + x2 + x3    # Linearity property
N = len(x)

X = np.fft.fft(x)
freqs = np.fft.fftfreq(N, d=1 / fs)
X_shifted = np.fft.fftshift(X)
freqs_shifted = np.fft.fftshift(freqs)
magnitude = np.abs(X_shifted)

fig, axes = plt.subplots(2, 1, figsize=(10, 7))

axes[0].plot(t, x)
axes[0].set_xlabel("time (s)")
axes[0].set_ylabel("amplitude")
axes[0].set_title("time domain: sum of three sine waves")
axes[0].set_xlim(0, 0.1)
axes[0].grid(True)

axes[1].plot(freqs_shifted, magnitude)
axes[1].set_xlabel("frequency (Hz)")
axes[1].set_ylabel("magnitude")
axes[1].set_title("frequency domain: FFT")
axes[1].set_xlim(-400, 400)
axes[1].grid(True)

fig.tight_layout()
fig.savefig("week1/d04_fft_multi.png", dpi=120)
print("saved to d04_fft_multi.png")

for f_expected in [f1, f2, f3]:
    idx = np.argmin(np.abs(freqs_shifted - f_expected))
    print(f"f={f_expected} Hz -> magnitude={magnitude[idx]:.2f}")