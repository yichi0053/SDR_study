import matplotlib.pyplot as plt
import numpy as np


def make_sine(f, fs, duration, amp=1.0, phase=0.0):
    n = np.arange(int(fs * duration))
    t = n / fs
    x = amp * np.sin(2 * np.pi * f * t + phase)
    return t, x


f_signal = 7000.0
fs = 10000.0
duration = 0.005

fs_ref = 500000.0
t_ref, x_ref = make_sine(f_signal, fs_ref, duration)

t, x = make_sine(f_signal, fs, duration)

duration_fft = 0.1
t_fft, x_fft = make_sine(f_signal, fs, duration_fft)    # Improve frequency resolution
N = len(x_fft)

X = np.fft.fftshift(np.fft.fft(x_fft))
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))
magnitude = np.abs(X)

positive_mask = freqs >= 0
peak_idx = np.argmax(magnitude[positive_mask])
peak_freq = freqs[positive_mask][peak_idx]

print("f        =", f_signal, "Hz")
print("fs       =", fs, "Hz")
print("Nyquist frequency      =", fs / 2, "Hz")
print("Theoretical aliasing frequency    =", fs - f_signal, "Hz")
print("Peak detected by FFT   =", peak_freq, "Hz")

f_alias = fs - f_signal
_, x_alias_ref = make_sine(f_alias, fs_ref, duration)

fig, axes = plt.subplots(2, 1, figsize=(11, 8))

axes[0].plot(t_ref * 1000, x_ref, color="C0", linewidth=0.8,
             alpha=0.5, label=f"original {f_signal/1000:g} kHz")
axes[0].plot(t_ref * 1000, x_alias_ref, color="C2", linewidth=1.2,
             linestyle="--", alpha=0.7, label=f"alias {f_alias/1000:g} kHz")
axes[0].stem(t * 1000, x, linefmt="C1-", markerfmt="C1o", basefmt=" ",
             label=f"samples at fs={fs/1000:g} kHz")
axes[0].set_xlabel("time (ms)")
axes[0].set_ylabel("amplitude")
axes[0].set_title("time domain: samples fit the alias frequency too")
axes[0].set_ylim(-1.3, 1.3)
axes[0].legend(loc="upper right", fontsize=8)
axes[0].grid(True, alpha=0.3)

axes[1].plot(freqs / 1000, magnitude)
# Vertical reference line
axes[1].axvline(f_alias / 1000, color="C3", linestyle="--",
                alpha=0.7, label=f"predicted alias {f_alias/1000:g} kHz")
axes[1].set_xlabel("frequency (kHz)")
axes[1].set_ylabel("magnitude")
axes[1].set_title("frequency domain: peak appears at the alias frequency")
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("week1/d06_alias_demo.png", dpi=120)
print("saved to d06_alias_demo.png")