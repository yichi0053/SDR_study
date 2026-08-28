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

f_spec, t_spec, Sxx = spectrogram(x, fs, nperseg=256, noverlap=128) # nperseg -> n per segment for FFT
                                                                    # noverlap -> overlap n per segment for smoother sampling
Sxx_db = 10 * np.log10(Sxx + 1e-12)

fig, ax = plt.subplots(figsize=(10, 6))
pcm = ax.pcolormesh(t_spec, f_spec, Sxx_db, shading="gouraud")
ax.set_xlabel("time (s)")
ax.set_ylabel("frequency (Hz)")
ax.set_title(f"spectrogram: chirp from {f0} Hz to {f1} Hz clearly visible over time")
fig.colorbar(pcm, ax=ax, label="power (dB)")

fig.tight_layout()
fig.savefig("week1/d10_spectrogram.png", dpi=120)
print("saved to d10_spectrogram.png")
print("frequency bins:", len(f_spec), ", time bins:", len(t_spec))