import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin

sample_rate = 32000
cutoff = 3000

fig, axes = plt.subplots(2, 1, figsize=(10, 6))

for num_taps in [11, 51, 101]:
    h = firwin(num_taps, cutoff, fs=sample_rate)

    axes[0].plot(h, '.-', label=f"num_taps={num_taps}")

    H = np.abs(np.fft.fftshift(np.fft.fft(h, 1024)))
    w = np.linspace(-sample_rate/2, sample_rate/2, len(H))
    axes[1].plot(w, H, label=f"num_taps={num_taps}")

axes[0].set_title("impulse response (taps)")
axes[0].legend()

axes[1].set_title("frequency response")
axes[1].set_xlim(0, sample_rate/2)
axes[1].set_xlabel("frequency (Hz)")
axes[1].legend()

plt.tight_layout()
plt.savefig("d29_firwin_design.png", dpi=120)
print("saved")