# The spectrum of a complex exponential signal does not 
# exhibit positive-negative frequency symmetry (mirroring); 
# instead, a peak appears on only one side.
import matplotlib.pyplot as plt
import numpy as np


fs = 1000.0
duration = 1.0
f = 50.0

n = np.arange(int(fs * duration))
t = n / fs

x_real = np.sin(2 * np.pi * f * t)
x_complex = np.exp(1j * 2 * np.pi * f * t).astype(np.complex64)

N = len(t)
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))

X_real = np.fft.fftshift(np.fft.fft(x_real))
X_complex = np.fft.fftshift(np.fft.fft(x_complex))

mag_real = np.abs(X_real)
mag_complex = np.abs(X_complex)

fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

axes[0].plot(freqs, mag_real, color="C0")
axes[0].set_ylabel("magnitude")
axes[0].set_title("FFT of REAL signal sin(2*pi*f*t): symmetric, peaks at +f and -f")
axes[0].grid(True, alpha=0.3)

axes[1].plot(freqs, mag_complex, color="C1")
axes[1].set_xlabel("frequency (Hz)")
axes[1].set_ylabel("magnitude")
axes[1].set_title("FFT of COMPLEX signal exp(j*2*pi*f*t): only +f has a peak")
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d17_complex_fft.png", dpi=120)
print("saved to d17_complex_fft.png")

positive_mask = freqs >= 0
negative_mask = freqs < 0

real_positive_peak = mag_real[positive_mask].max()
real_negative_peak = mag_real[negative_mask].max()
complex_positive_peak = mag_complex[positive_mask].max()
complex_negative_peak = mag_complex[negative_mask].max()

print("real signal:    positive-side peak =", real_positive_peak,
      ", negative-side peak =", real_negative_peak)
print("complex signal: positive-side peak =", complex_positive_peak,
      ", negative-side peak =", complex_negative_peak)