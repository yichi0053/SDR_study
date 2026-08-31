# Generate a complex exponential signal,
# plot its I/Q separately.
import matplotlib.pyplot as plt
import numpy as np


fs = 1000.0
duration = 0.05
f = 50.0

n = np.arange(int(fs * duration))
t = n / fs

x = np.exp(1j * 2 * np.pi * f * t).astype(np.complex64) # e^(jθ)

i_component = x.real    # I
q_component = x.imag    # Q

print("dtype of x   =", x.dtype)
print("x[0]         =", x[0])
print("x[5]         =", x[5])
print("magnitude of x[5] =", np.abs(x[5]))  # -> sqrt(real² + imag²) -> cos²(θ)+sin²(θ)=1

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axes[0].plot(t * 1000, i_component, label="I (real part, cos)", color="C0")
axes[0].plot(t * 1000, q_component, label="Q (imag part, sin)", color="C1")
axes[0].set_ylabel("amplitude")
axes[0].set_title(f"complex exponential signal, f={f} Hz, fs={fs} Hz")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(t * 1000, i_component, label="I", color="C0")
axes[1].plot(t * 1000, q_component, label="Q", color="C1")
axes[1].set_xlabel("time (ms)")
axes[1].set_ylabel("amplitude (zoomed)")
axes[1].set_xlim(0, 20) # zoom in
axes[1].legend()
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d15_complex_signal.png", dpi=120)
print("saved to d15_complex_signal.png")