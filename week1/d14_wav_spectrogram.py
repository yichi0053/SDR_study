import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram


filepath = "week1/sample.wav"

sample_rate, data = wavfile.read(filepath)

if data.ndim == 1:
    num_channels = 1
    audio = data
else:
    num_channels = data.shape[1] # type: ignore
    audio = data.mean(axis=1)   # Average all channels into a single channel.

# Normalization
max_value = np.iinfo(data.dtype).max    # iinfo -> Query information about the value range of an integer type.
audio_normalized = audio.astype(np.float64) / max_value # astype(float) -> turn to float type

nyquist = sample_rate / 2

f_spec, t_spec, Sxx = spectrogram(audio_normalized, sample_rate,
                                   nperseg=4096, noverlap=2048)     # Sxx's shape -> (n of frequency, n of time)
Sxx_db = 10 * np.log10(Sxx + 1e-12)

fig, ax = plt.subplots(figsize=(12, 6))
pcm = ax.pcolormesh(t_spec, f_spec, Sxx_db, shading="gouraud")
ax.set_xlabel("time (s)")
ax.set_ylabel("frequency (Hz)")
ax.set_title(f"spectrogram of {filepath} (sample_rate={sample_rate} Hz, "
             f"nyquist={nyquist} Hz)")
fig.colorbar(pcm, ax=ax, label="power (dB)")

fig.tight_layout()
fig.savefig("week1/d14_wav_spectrogram.png", dpi=120)
print("saved to d14_wav_spectrogram.png")

energy_per_bin = Sxx.max(axis=1)
threshold = energy_per_bin.max() * 0.01
above_threshold = f_spec[energy_per_bin > threshold]
if len(above_threshold) > 0:
    print("estimated highest frequency with meaningful energy =",
          above_threshold.max(), "Hz")
else:
    print("no frequency bin exceeded the energy threshold")