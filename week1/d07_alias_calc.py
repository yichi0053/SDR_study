# Given any f_signal and fs, calculate the aliasing frequency.
import numpy as np


# check if fs > 2*f
def predict_alias(f_signal, f_sample):
    nyquist = f_sample / 2
    f_folded = f_signal % f_sample
    if f_folded > nyquist:
        return f_sample - f_folded
    return f_folded


# Do FFT and return the maximum positive frequency.
def verify_by_fft(f_signal, f_sample, duration=0.1):
    n = np.arange(int(f_sample * duration))
    t = n / f_sample
    x = np.sin(2 * np.pi * f_signal * t)

    N = len(x)
    X = np.fft.fftshift(np.fft.fft(x))
    freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / f_sample))
    magnitude = np.abs(X)

    positive_mask = freqs >= 0
    peak_idx = np.argmax(magnitude[positive_mask])
    return freqs[positive_mask][peak_idx]


if __name__ == "__main__":
    fs = 10000.0
    test_cases = [3000.0, 5000.0, 6000.0, 7000.0,
                  10000.0, 12000.0, 17000.0, 23000.0]

    print(f"{'f (Hz)':>10} {'predicted':>12} {'fft peak':>12} {'match':>7}")
    print("-" * 45)

    for f in test_cases:
        predicted = predict_alias(f, fs)
        measured = verify_by_fft(f, fs)

        # FFT frequency resolution is fs/N = 10000/1000 = 10 Hz, so the measured
        # peak can only land on multiples of 10 Hz. Allow a 20 Hz tolerance
        # (about two bins) to account for this discretization, not for error.
        match = "OK" if abs(predicted - measured) < 20 else "MISMATCH"
        print(f"{f:>10.0f} {predicted:>12.1f} {measured:>12.1f} {match:>7}")


    # f = 5000, 10000 -> f/fs = 0.5, 1 -> sin()=0  -> MISMATCH