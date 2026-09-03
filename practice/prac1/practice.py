import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin, fftconvolve, spectrogram

"""
step 1 : read file
"""

# read file
filepath = "pulsed_ASK.sigmf-data"
sample = np.fromfile(filepath, dtype=np.complex64)
print("init_sample: ", len(sample))

sample = sample[int(len(sample)*0.2):int(len(sample)*0.3)]   # analyze first 2M samples (enough for pulsed signal)
sample = sample / np.max(np.abs(sample))
fs = 2.4e6   # 2.4 MHz
N = sample.shape[0] # or len()
duration = N / fs

print("number of sample: ", N)
print("sample rate: ", fs)
print("duration: ", duration)

# print(type(sample))
# print(sample.dtype)
# print(len(sample))
# print(sample.ndim, sample.shape)


"""
step 2 : check saturation
"""

# check saturation
sample_abs = np.abs(sample)
sample_max = np.max(sample_abs)
near_max = np.sum(sample_abs > sample_max * 0.99)
near_max_ratio = near_max / N

print("maximum: ", sample_max)
print(f"proportion near maximum: {near_max_ratio:.4f}")

if near_max_ratio > 0.01:
    print("==saturation==")
else:
    print("==no saturation==")


"""
step 3 : do PSD and noise floor
"""

# PSD: (FFT→ abs→ square→ divided by N·Fs→ 10log10 →fftshift)
X = np.fft.fft(sample)
psd = np.abs(X)
psd = psd ** 2
psd = psd / (N * fs)
psd_db = 10 * np.log10(psd + 1e-20)
psd_db = np.fft.fftshift(psd_db)
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1/fs))


# noise floor
noise_floor = np.median(psd_db)
threshold = noise_floor + 20
above_threshold = psd_db > threshold

# merge bin
signal_groups = []
in_group = False
num_above_threshold = len(above_threshold)
print("start merge bin...")
# find where above_threshold changes between True/False
above_int = above_threshold.astype(int)
diff = np.diff(above_int)          # +1 marks a rising edge (start), -1 marks a falling edge (end)

starts = np.where(diff == 1)[0] + 1   # indices where a group starts
ends = np.where(diff == -1)[0] + 1    # indices where a group ends

# handle edge cases: signal already above threshold at the very beginning
if above_threshold[0]:
    starts = np.insert(starts, 0, 0)
# handle edge case: signal still above threshold at the very end
if above_threshold[-1]:
    ends = np.append(ends, len(above_threshold))

signal_groups = list(zip(starts, ends))
print("group found: ",len(signal_groups) )

# for i in range(num_above_threshold):
#     if above_threshold[i] and not in_group:
#         start = i
#         in_group = True
#     elif not above_threshold[i] and in_group:
#         end = i
#         signal_groups.append((start, end))
#         in_group = False
# if in_group:
#     signal_groups.append((start, len(above_threshold)))


"""
step 4 : check DC spike
"""

# DC spike
def find_center_freq(group_start, group_end, freqs):
    return freqs[group_start:group_end][np.argmax(psd_db[group_start:group_end])]


signals = []
dc_spike_found = False
freq_res = fs / N

for (start, end) in signal_groups:
    center_freq = find_center_freq(start, end, freqs)
    width_bins = end - start

    near_dc = abs(center_freq) < (freq_res) * 5   # (fs / N) * 5 = 0 +- bin(frequency resolution)*5
    is_narrow = width_bins <= 3

    if near_dc and is_narrow:
        dc_spike_found = True
        print(f"Excluded DC spike at {center_freq:.1f} Hz (width={width_bins} bins)")
        continue

    signals.append({"center_freq": center_freq, "start": start, "end": end})


"""
step 5 : move to baseband
"""
t = np.arange(N) / fs

# move to baseband
for sig in signals:
    f_center = sig["center_freq"]
    bandwidth_hz = (sig["end"] - sig["start"]) * (freq_res)

    shifted = sample * np.exp(-1j * 2 * np.pi * f_center * t)

    cutoff = bandwidth_hz / 2 * 1.2     # transition width
    cutoff = min(cutoff, fs / 2 * 0.9)
    h = firwin(101, cutoff, fs=fs)
    filtered = fftconvolve(shifted, h, mode='same')

    sig["baseband"] = filtered
    sig["bandwidth_hz"] = bandwidth_hz


"""
step 6 : filter and decimation
"""

for sig in signals:
    # choose decimation factor: new sample rate must comfortably exceed the signal bandwidth
    # target new_fs = 4x cutoff (2x for Nyquist + 2x safety margin)
    target_fs = sig["bandwidth_hz"] * 4
    decim = max(1, int(fs / target_fs))          # at least 1, must be integer
    decim = min(decim, 100)                        # cap to avoid over-decimation

    sig["baseband"] = sig["baseband"][::decim]     # decimate the already-filtered signal
    sig["fs_new"] = fs / decim

"""
step 7 : determine modulation
"""

def guess_modulation(baseband_signal):
    sub = baseband_signal[::10]
    # phase distribution
    phases_deg = np.angle(sub, deg=True) % 360
    # magnitude distribution
    mags = np.abs(sub)
    # number of peak
    hist, bin_edges = np.histogram(phases_deg, bins=36, range=(0, 360))
    peak_threshold = hist.max() * 0.3
    num_peaks = np.sum(hist > peak_threshold)
    # degree of discrete
    mag_std = np.std(mags) / (np.mean(mags) + 1e-9)

    if mag_std > 0.5:
        return "uncertain (magnitude too scattered, possibly FSK or noise, check spectrogram)"
    elif num_peaks <= 3:
        return "BPSK (2 clusters)"
    elif num_peaks <= 6:
        return "QPSK (4 clusters)"
    else:
        return "uncertain (many/no clear clusters, possibly QAM, FSK, or noise)"

for sig in signals:
    sig["modulation_guess"] = guess_modulation(sig["baseband"])


"""
step 8 : analyze
"""
print("\n=== Analysis Report:", filepath, "===")
print(f"Sample rate: {fs:,.0f} Hz (assumed)")

# saturation
sat_status = "LIKELY SATURATED" if near_max_ratio > 0.01 else "PASS"
print(f"Saturation check: {sat_status} (max |sample| = {sample_max:.2f})")

# no signal detected 
if len(signals) == 0:
    print("Detected signals: 0")
    print("Conclusion: no signal above noise floor detected — this capture may contain only noise.")
else:
    print(f"Detected signals: {len(signals)}")
    for i, sig in enumerate(signals, 1):
        print(f"  Signal {i}: center freq ~ {sig['center_freq']:,.0f} Hz, "
              f"bandwidth ~ {sig['bandwidth_hz']:,.0f} Hz, "
              f"estimated modulation: {sig['modulation_guess']}")

# DC spike
print(f"DC spike detected at 0 Hz: {'YES' if dc_spike_found else 'NO'}")


"""
diagram
"""
# PSD
plt.figure(figsize=(12, 5))
plt.plot(freqs / 1e3, psd_db)
plt.axhline(threshold, color='r', linestyle='--', label='threshold')
plt.xlabel("frequency (kHz)")
plt.ylabel("power (dB)")
plt.title("PSD of pulsed_ASK")
plt.legend()
plt.grid(True)
plt.savefig("analysis_psd.png", dpi=120)

# spectrogram
f_spec, t_spec, Sxx = spectrogram(sample, fs, nperseg=1024,
                                   return_onesided=False)
Sxx_db = 10 * np.log10(np.fft.fftshift(Sxx, axes=0) + 1e-12)
f_spec = np.fft.fftshift(f_spec)

plt.figure(figsize=(12, 6))
plt.pcolormesh(t_spec, f_spec / 1e3, Sxx_db, shading='gouraud')
plt.xlabel("time (s)")
plt.ylabel("frequency (kHz)")
plt.title("spectrogram of pulsed_ASK")
plt.colorbar(label="power (dB)")
plt.savefig("analysis_spectrogram.png", dpi=120)

# constellation
for i, sig in enumerate(signals, 1):
    bb = sig["baseband"]
    plt.figure(figsize=(6, 6))
    plt.plot(np.real(bb), np.imag(bb), '.', markersize=1)
    plt.xlabel("I")
    plt.ylabel("Q")
    plt.title(f"constellation of signal {i}")
    plt.axis('equal')
    plt.grid(True)
    plt.savefig(f"analysis_constellation_{i}.png", dpi=120)