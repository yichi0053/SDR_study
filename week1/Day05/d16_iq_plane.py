# Implement phasor diagram
import matplotlib.pyplot as plt
import numpy as np


fs = 1000.0
duration = 0.02
f = 50.0

n = np.arange(int(fs * duration))
t = n / fs

x = np.exp(1j * 2 * np.pi * f * t).astype(np.complex64)

i_component = np.real(x)
q_component = np.imag(x)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(t * 1000, i_component, label="I", color="C0")
axes[0].plot(t * 1000, q_component, label="Q", color="C1")
axes[0].set_xlabel("time (ms)")
axes[0].set_ylabel("amplitude")
axes[0].set_title("time domain: I and Q vs time")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(i_component, q_component, marker="o", markersize=3,
             linestyle="-", linewidth=0.8, color="C2")
axes[1].plot(i_component[0], q_component[0], marker="*",
             markersize=15, color="red", label="start (t=0)")
axes[1].set_xlabel("I (real part)")
axes[1].set_ylabel("Q (imaginary part)")
axes[1].set_title("IQ plane: complex exponential traces a circle")
axes[1].set_xlim(-1.3, 1.3)
axes[1].set_ylim(-1.3, 1.3)
axes[1].set_aspect("equal") # Force the unit lengths on the x-axis and y-axis appear visually identical.
axes[1].legend()
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d16_iq_plane.png", dpi=120)
print("saved to d16_iq_plane.png")

radius = np.sqrt(i_component**2 + q_component**2)
print("radius (should all be ~1.0):")
print("  min =", radius.min())
print("  max =", radius.max())