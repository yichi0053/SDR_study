import numpy as np
from scipy.io import wavfile


filepath = "../../sample.wav"

sample_rate, data = wavfile.read(filepath)  # sample_rate = RIFF/fmt chunk/SampleRate
                                            # data = RIFF/data chunk

print("\nsample rate\t=", sample_rate, "Hz")
print("data dtype\t=", data.dtype)  # bit depth
print("data shape\t=", data.shape)

if data.ndim == 1:                  # mono: (num_samples)
    num_channels = 1
    num_samples = data.shape[0]
else:                               # stereo: (num_samples, num_channels)
    num_samples, num_channels = data.shape # type: ignore[misc]

print("number of channels  =", num_channels)
print("number of samples   =", num_samples)

bytes_per_sample = data.dtype.itemsize
print("bytes per sample    =", bytes_per_sample)

duration = num_samples / sample_rate
print("duration            =", duration, "seconds")

nyquist = sample_rate / 2
print("Nyquist frequency   =", nyquist, "Hz")