# SNR (Signal-to-Noise Ratio) = P_signal / P_noise
import matplotlib.pyplot as plt
import numpy as np

N = 1000
fs = 1000.0

# unit power signal
t = np.arange(N) / fs
signal = np.exp(1j * 2 * np.pi * 50 * t)

snr_db = 10
noise_power = 10 ** (-snr_db / 10)  # signal power is 1, so this gives SNR = snr_db

noise = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2) * np.sqrt(noise_power)

r = signal + noise

measured_snr = np.var(signal) / np.var(noise)
print("target SNR (dB):", snr_db)
print("measured SNR (dB):", 10 * np.log10(measured_snr))

psd = np.abs(np.fft.fftshift(np.fft.fft(r))) ** 2 / (N * fs)
psd_db = 10 * np.log10(psd)
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1/fs))

plt.plot(freqs, psd_db)
plt.xlabel("frequency (Hz)")
plt.ylabel("power (dB)")
plt.title(f"PSD at SNR = {snr_db} dB")
plt.savefig("d25_snr.png", dpi=120)
print("saved")