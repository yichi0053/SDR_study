# Compare three different nperseg
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp, spectrogram


fs = 10000.0
duration = 1.0
f0 = 100.0
f1 = 4000.0

n = np.arange(int(fs * duration))
t = n / fs
x = chirp(t, f0=f0, f1=f1, t1=duration, method="linear")

nperseg_list = [64, 256, 1024]

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)    # sharey -> share y axis

for ax, nperseg in zip(axes, nperseg_list):
    noverlap = nperseg // 2
    f_spec, t_spec, Sxx = spectrogram(x, fs, nperseg=nperseg, noverlap=noverlap)
    Sxx_db = 10 * np.log10(Sxx + 1e-12)

    freq_resolution = fs / nperseg
    time_resolution = nperseg / fs

    ax.pcolormesh(t_spec, f_spec, Sxx_db, shading="gouraud")
    ax.set_xlabel("time (s)")
    ax.set_title(f"nperseg={nperseg}\n"
                 f"freq res={freq_resolution:.1f} Hz, "
                 f"time res={time_resolution*1000:.1f} ms")

axes[0].set_ylabel("frequency (Hz)")

fig.suptitle("Time-Frequency Tradeoff: smaller nperseg = finer time, coarser frequency")
fig.tight_layout()
fig.savefig("d11_resolution_tradeoff.png", dpi=120)
print("saved to d11_resolution_tradeoff.png")

for nperseg in nperseg_list:
    print(f"nperseg={nperseg}: freq_resolution={fs/nperseg:.2f} Hz, "
          f"time_resolution={nperseg/fs*1000:.2f} ms")