import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt


fs = 10000.0
fs_analog = 500000.0
duration = 0.1

f_wanted = 2000.0
f_interferer = 7000.0

n_analog = np.arange(int(fs_analog * duration))
t_analog = n_analog / fs_analog
# Simulating interference signals in real-world scenarios
x_analog = (np.sin(2 * np.pi * f_wanted * t_analog)
            + 0.8 * np.sin(2 * np.pi * f_interferer * t_analog))

cutoff = fs / 2 * 0.8   # Sean's 4/5 rule
sos = butter(N=8, Wn=cutoff, btype="low", fs=fs_analog, output="sos") # btype=low -> low-pass filter
x_filtered = sosfiltfilt(sos, x_analog)

decim = int(fs_analog / fs) # Simulate "switching to a lower sampling rate (fs)"
x_no_filter = x_analog[::decim]
x_with_filter = x_filtered[::decim]

N = len(x_no_filter)
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / fs))

mag_no_filter = np.abs(np.fft.fftshift(np.fft.fft(x_no_filter)))
mag_with_filter = np.abs(np.fft.fftshift(np.fft.fft(x_with_filter)))

f_alias = fs - f_interferer

print("f_wanted     =", f_wanted, "Hz")
print("f_interferer   =", f_interferer, "Hz")
print("Nyquist frequency       =", fs / 2, "Hz")
print("Aliasing location of f_interferer  =", f_alias, "Hz")
print("cutoff       =", cutoff, "Hz")

fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

axes[0].plot(freqs / 1000, mag_no_filter, color="C1")
axes[0].axvline(f_wanted / 1000, color="C0", linestyle="--",
                alpha=0.6, label=f"wanted {f_wanted/1000:g} kHz")
axes[0].axvline(f_alias / 1000, color="C3", linestyle="--",
                alpha=0.6, label=f"alias of {f_interferer/1000:g} kHz")
axes[0].set_ylabel("magnitude")
axes[0].set_title("without anti-aliasing filter")
axes[0].legend(fontsize=8)
axes[0].grid(True, alpha=0.3)

axes[1].plot(freqs / 1000, mag_with_filter, color="C2")
axes[1].axvline(f_wanted / 1000, color="C0", linestyle="--",
                alpha=0.6, label=f"wanted {f_wanted/1000:g} kHz")
axes[1].axvline(f_alias / 1000, color="C3", linestyle="--",
                alpha=0.6, label=f"alias location (now suppressed)")
axes[1].set_xlabel("frequency (kHz)")
axes[1].set_ylabel("magnitude")
axes[1].set_title("with anti-aliasing filter before sampling")
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d08_antialias.png", dpi=120)
print("saved to d08_antialias.png")