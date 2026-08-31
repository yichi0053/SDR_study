# /usr/bin python
import matplotlib.pyplot as plt
import numpy as np


def make_sine(f, fs, duration, amp=1.0, phase=np.pi / 2):
    n = np.arange(int(fs * duration))
    t = n / fs  # vectorization
    x = amp * np.sin(2 * np.pi * f * t + phase)  # amplitude
    return t, x


if __name__ == "__main__":
    f = 5.0
    fs = 1000.0
    duration = 1.0

    t, x = make_sine(f, fs, duration)

    # If the condition is not met, throw an error and stop immediately.
    assert len(x) == int(fs * duration)

    print("N (sample size)\t\t  =", len(x))
    print("normalized frequency f/fs =", f / fs)
    print("samples per cycle fs/f    =", fs / f)

    plt.figure(figsize=(10, 4))
    plt.plot(t, x)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")
    plt.title(f"sine wave: f={f} Hz, fs={fs} Hz")
    plt.grid(True)
    plt.savefig("d01_sine.png", dpi=120)
    print("saved to d01_sine.png")

