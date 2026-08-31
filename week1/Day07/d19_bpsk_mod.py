# BPSK Modulation
import matplotlib.pyplot as plt
import numpy as np


np.random.seed(0)   # Fix the initial state of the random number generator.

num_bits = 20
bits = np.random.randint(0, 2, num_bits)

sps = 20    # samples_per_bit
fc = 5.0    # carrier_frequency
fs = 1000.0

symbols = 2 * bits - 1  # Turn {0, 1} to {-1, 1}

samples_per_bit = np.repeat(symbols, sps)

n = np.arange(len(samples_per_bit))
t = n / fs
carrier = np.cos(2 * np.pi * fc * t)

bpsk_signal = samples_per_bit * carrier

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axes[0].step(t, np.repeat(bits, sps), where="post", color="C0") # step() -> stepped line
                                                                # where="post" -> Specify the step change occurs after the data point.
axes[0].set_ylabel("bit value")
axes[0].set_title("original bits (0 or 1)")
axes[0].set_ylim(-0.3, 1.3)
axes[0].grid(True, alpha=0.3)

axes[1].step(t, samples_per_bit, where="post", color="C1")
axes[1].set_ylabel("symbol value")
axes[1].set_title("symbols after mapping (0->-1, 1->+1)")
axes[1].set_ylim(-1.3, 1.3)
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, bpsk_signal, color="C2", linewidth=0.8)
axes[2].set_xlabel("time (s)")
axes[2].set_ylabel("amplitude")
axes[2].set_title(f"BPSK modulated signal (carrier fc={fc} Hz, sps={sps})")
axes[2].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("d19_bpsk_mod.png", dpi=120)
print("saved to d19_bpsk_mod.png")

print("original bits:", bits)
print("mapped symbols:", symbols)