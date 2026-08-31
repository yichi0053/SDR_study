# /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np


def make_sine(f, fs, duration, amp=1.0, phase=np.pi / 2):
    n = np.arange(int(fs * duration))
    t = n / fs  # vectorization
    x = amp * np.sin(2 * np.pi * f * t + phase)  # amplitude
    return t, x


if __name__ == "__main__":
    f = 100.0
    duration = 0.1
    fs_ref = 20000.0  # reference sampling frequency
    fs_list = [2000, 500, 200, 150, 100, 50]  # Nyquist frequency: fs/f = 2

    t_ref, x_ref = make_sine(
        f, fs_ref, duration
    )  # use as background reference lines in each subplots

    fig, axes = plt.subplots(2, 3, figsize=(15, 7))  # create a figure and subplots

    for ax, fs in zip(axes.flat, fs_list):  # flatten a 2D array into a 1D sequence
        t, x = make_sine(f, fs, duration)
        ax.plot(
            t_ref, x_ref, color="C0", linewidth=0.8, alpha=0.5
        )  # backgroung reference lines
        ax.stem(t, x, linefmt="C1-", markerfmt="C1o", basefmt=" ")
        ax.set_title(
            f"fs={fs} Hz, fs/f={fs / f:g}, N={len(x)}"
        )  # ":g" is a format specifier, automatically remove excess decimal places.
        ax.set_ylim(-1.3, 1.3)
        ax.set_xlabel("time (s)")
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("d02_undersample.png", dpi=120)  # dot per inch
    print("saved to d02_undersample.png")
