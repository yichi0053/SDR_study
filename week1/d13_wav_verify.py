import os
from scipy.io import wavfile


filepath = "week1/sample.wav"

sample_rate, data = wavfile.read(filepath)

if data.ndim == 1:
    num_channels = 1
    num_samples = data.shape[0]
else:
    num_samples, num_channels = data.shape # type: ignore[misc]

bytes_per_sample = data.dtype.itemsize

audio_data_size = num_samples * num_channels * bytes_per_sample
standard_header_size = 44
theoretical_size = standard_header_size + audio_data_size

actual_size = os.path.getsize(filepath)

difference = actual_size - theoretical_size

print("\n")
print("num_samples           =", num_samples)
print("num_channels          =", num_channels)
print("bytes_per_sample      =", bytes_per_sample)
print("audio_data_size       =", audio_data_size, "bytes")
print("theoretical_size (44-byte header) =", theoretical_size, "bytes")
print("actual_size (os.path.getsize)     =", actual_size, "bytes")
print("difference            =", difference, "bytes")

if difference == 0:
    print("result: matches the standard 44-byte header exactly")
else:
    print("result: mismatch — this file likely contains extra")
    print("        non-essential chunks beyond the minimal 44-byte header")