# Implement the complete "PSD Six-Step Process".
# Compute FFT → Take absolute value → Square → Normalize → Convert to dB → fftshift
import matplotlib.pyplot as plt
import numpy as np


Fs = 1e6
N = 2048
Ts = 1 / Fs
t = Ts * np.arange(N)

f_signal = 50e3
x = np.exp(1j * 2 * np.pi * f_signal * t)

# Generate complex Gaussian white noise
noise_power = 2
n = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2) # sqrt(2)： Normalize average power to 1

r = x + n * np.sqrt(noise_power)    # sqrt(noise_power) : Power is (Amplitude)^2

dc_leakage = 0.5
r_with_dc = r + dc_leakage

def compute_psd(samples, fs, n_fft):
    X = np.fft.fft(samples, n_fft)          # FFT
    psd = np.abs(X) ** 2 / (n_fft * fs)     # absolutely value, Square, Normalization
    psd_db = 10.0 * np.log10(psd)           # to dB
    psd_shifted = np.fft.fftshift(psd_db)   # fftshift
    return psd_shifted

psd_clean = compute_psd(r, Fs, N)
psd_dc = compute_psd(r_with_dc, Fs, N)

freqs = np.arange(Fs / -2.0, Fs / 2.0, Fs / N)

fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

axes[0].plot(freqs / 1e3, psd_clean, color="C0")
axes[0].set_ylabel("power (dB)")
axes[0].set_title(f"PSD: complex exponential at {f_signal/1e3:.0f} kHz + AWGN") # AWGN (Additive White Gaussian Noise)
axes[0].grid(True, alpha=0.3)

axes[1].plot(freqs / 1e3, psd_dc, color="C3")
axes[1].set_xlabel("frequency (kHz)")
axes[1].set_ylabel("power (dB)")
axes[1].set_title("PSD: same signal with simulated DC leakage (LO leakage)")
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d18b_psd.png", dpi=120)
print("saved to d18b_psd.png")

avg_pwr_var = np.var(r)
avg_pwr_formula = np.mean(np.abs(r) ** 2)
print("average power (np.var)          =", avg_pwr_var)
print("average power (mean of |x|^2)   =", avg_pwr_formula)
print("signal mean (should be ~0)      =", np.mean(r))