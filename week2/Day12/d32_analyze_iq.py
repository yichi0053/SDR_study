import matplotlib.pyplot as plt
import numpy as np

# --- create a more realistic test file: signal offset from 0 Hz, plus noise ---
fs = 1e6
N = 20000
t = np.arange(N) / fs

f_offset = 150e3
num_symbols = N // 20
x_int = np.random.randint(0, 4, num_symbols)
x_radians = (x_int * 360 / 4.0 + 45) * np.pi / 180.0
symbols = np.cos(x_radians) + 1j * np.sin(x_radians)
baseband = np.repeat(symbols, 20)

sig = baseband * np.exp(1j * 2 * np.pi * f_offset * t)
noise = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2) * np.sqrt(0.05)
r = (sig + noise).astype(np.complex64)
r.tofile('mystery.iq')

# --- pretend we know nothing except the sample rate ---
samples = np.fromfile('mystery.iq', np.complex64)

print("num samples:", len(samples))
print("max |sample|:", np.max(np.abs(samples)))

# PSD, 6-step process
X = np.fft.fft(samples)
psd = np.abs(X) ** 2 / (len(samples) * fs)
psd_db = 10 * np.log10(psd)
psd_db = np.fft.fftshift(psd_db)
freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), d=1/fs))

plt.figure()
plt.plot(freqs / 1e3, psd_db)
plt.xlabel("frequency (kHz)")
plt.ylabel("power (dB)")
plt.title("PSD of mystery.iq")
plt.savefig("d32_analyze_iq_psd.png", dpi=120)

peak_freq = freqs[np.argmax(psd_db)]
print("detected signal peak at:", peak_freq, "Hz")

# demodulate down to baseband using the detected peak, then look at constellation
r_baseband = samples * np.exp(-1j * 2 * np.pi * peak_freq * t)
plt.figure()
plt.plot(np.real(r_baseband[::20]), np.imag(r_baseband[::20]), '.')
plt.grid(True)
plt.title("constellation after shifting detected signal to baseband")
plt.savefig("d32_analyze_iq_constellation.png", dpi=120)
print("saved")