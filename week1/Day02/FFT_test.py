import matplotlib.pyplot as plt
import numpy as np

fs = 1
N = 100  # number of points to simulate, and our FFT size

t = np.arange(N / fs)
s = np.sin(2 * np.pi * 0.15 * t)
S = np.fft.fftshift(np.fft.fft(s))
S_mag = np.abs(S)  # a function for magnitude of a complex number
S_phase = np.angle(S)  # the phase in units of radians
f = np.arange(fs / -2, fs / 2, fs / N)
plt.figure(0)
plt.plot(f, S_mag, ".-")
plt.figure(1)
plt.plot(f, S_phase, ".-")
plt.show()
