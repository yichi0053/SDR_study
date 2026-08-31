# Asymmetry between positive and negative frequencies in complex sampling
#Verify that the effective bandwidth of complex sampling is equal to the sampling rate itself (fs).
import matplotlib.pyplot as plt
import numpy as np


fs = 1000.0
duration = 1.0
n = np.arange(int(fs * duration))
t = n / fs

f_test_list = [100.0, 300.0, 490.0]

fig, axes = plt.subplots(2, len(f_test_list), figsize=(15, 7), sharex=True)

for col, f_test in enumerate(f_test_list):  # enumerate -> (index, value)
    x_real = np.cos(2 * np.pi * f_test * t)
    x_complex = np.exp(1j * 2 * np.pi * f_test * t).astype(np.complex64)

    N = len(t)
    freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))

    mag_real = np.abs(np.fft.fftshift(np.fft.fft(x_real)))
    mag_complex = np.abs(np.fft.fftshift(np.fft.fft(x_complex)))

    axes[0, col].plot(freqs, mag_real, color="C0")
    axes[0, col].set_title(f"real, f={f_test} Hz")
    axes[0, col].grid(True, alpha=0.3)

    axes[1, col].plot(freqs, mag_complex, color="C1")
    axes[1, col].set_title(f"complex, f={f_test} Hz")
    axes[1, col].set_xlabel("frequency (Hz)")
    axes[1, col].grid(True, alpha=0.3)

axes[0, 0].set_ylabel("magnitude (real)")
axes[1, 0].set_ylabel("magnitude (complex)")

fig.suptitle(f"real signals only use 0 to fs/2 = {fs/2} Hz effectively\n"
             f"complex signals use the full -fs/2 to fs/2 = {fs} Hz")
fig.tight_layout()
fig.savefig("d18_bandwidth.png", dpi=120)
print("saved to d18_bandwidth.png")

print("\nreal signal f=490Hz: check if this is close to Nyquist edge (fs/2=500Hz)")
print("complex signal f=490Hz: should show single clean peak near edge, no aliasing yet")

# By using complex sampling at the same sampling rate, 
# it is possible to accommodate twice the amount of information within the effective bandwidth.