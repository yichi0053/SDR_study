# Constellation
import matplotlib.pyplot as plt
import numpy as np


np.random.seed(0)

num_symbols = 200

bits = np.random.randint(0, 2, num_symbols)
symbols = 2 * bits - 1

x_symbols = symbols.astype(np.complex64)    # Turn into complex number.

fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(np.real(x_symbols), np.imag(x_symbols), ".", markersize=10, color="C0")
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel("I (in-phase)")
ax.set_ylabel("Q (quadrature)")
ax.set_title(f"BPSK constellation ({num_symbols} symbols)")
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d20_constellation.png", dpi=120)
print("saved to d20_constellation.png")

unique_points = np.unique(x_symbols)
print("unique constellation points:", unique_points)
print("expected: [-1.+0.j  1.+0.j]")