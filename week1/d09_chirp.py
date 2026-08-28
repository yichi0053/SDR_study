# Looking at either the time domain or the FFT alone
# is insufficient to fully describe this signal.
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp  # sin(2π·(f0·t + (k/2)·t²))


fs = 10000.0
duration = 1.0
f0 = 100.0
f1 = 4000.0

n = np.arange(int(fs * duration))
t = n / fs

x = chirp(t, f0=f0, f1=f1, t1=duration, method="linear")

N = len(x)
X = np.fft.fftshift(np.fft.fft(x))
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))
magnitude = np.abs(X)

fig, axes = plt.subplots(2, 1, figsize=(11, 7))

axes[0].plot(t, x, linewidth=0.6)
axes[0].set_xlabel("time (s)")
axes[0].set_ylabel("amplitude")
axes[0].set_title(f"time domain: linear chirp from {f0} Hz to {f1} Hz")
axes[0].grid(True, alpha=0.3)

axes[1].plot(freqs, magnitude)
axes[1].set_xlim(0, fs / 2)
axes[1].set_xlabel("frequency (Hz)")
axes[1].set_ylabel("magnitude")
axes[1].set_title("frequency domain: FFT cannot show WHEN each frequency occurred")
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("week1/d09_chirp.png", dpi=120)
print("saved to d09_chirp.png")
print("signal duration:", duration, "s, frequency sweeps from", f0, "Hz to", f1, "Hz")