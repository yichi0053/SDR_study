import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin, fftconvolve

sample_rate = 32000
N = 5000
t = np.arange(N) / sample_rate

# wanted signal near 0 Hz, interferer at 10 kHz, plus noise
wanted = np.exp(1j * 2 * np.pi * 500 * t)
interferer = np.exp(1j * 2 * np.pi * 10000 * t)
noise = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2)

x = wanted + interferer + 0.5 * noise

h = firwin(101, 3000, fs=sample_rate)

y = fftconvolve(x, h, mode='same')

def psd(signal):
    return 10 * np.log10(np.fft.fftshift(np.abs(np.fft.fft(signal)) ** 2) / len(signal))

freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1/sample_rate))

plt.plot(freqs, psd(x), alpha=0.7, label="before filtering")
plt.plot(freqs, psd(y), alpha=0.7, label="after filtering")
plt.xlabel("frequency (Hz)")
plt.ylabel("PSD (dB)")
plt.legend()
plt.title("low-pass filter removes the 10kHz interferer")
plt.savefig("d30_filter_apply.png", dpi=120)
print("saved")