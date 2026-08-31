# BER (Bit Error Rate)
import matplotlib.pyplot as plt
import numpy as np

num_symbols = 10000

x_int = np.random.randint(0, 4, num_symbols)
x_degrees = x_int * 360 / 4.0 + 45
x_radians = x_degrees * np.pi / 180.0
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)

snr_db_list = np.arange(-5, 16, 2)  # Scan -5 to 15 dB, 2 dB intervals.
ber_list = []

for snr_db in snr_db_list:
    noise_power = 10 ** (-snr_db / 10)
    noise = (np.random.randn(num_symbols) + 1j * np.random.randn(num_symbols)) / np.sqrt(2) * np.sqrt(noise_power)
    r = x_symbols + noise

    # decide which quadrant each received point falls in
    r_degrees = np.angle(r, deg=True) % 360
    x_int_hat = np.floor(r_degrees / 90).astype(int)

    num_errors = np.sum(x_int_hat != x_int)
    ber = num_errors / num_symbols
    ber_list.append(ber)
    print(f"SNR = {snr_db} dB, errors = {num_errors}, BER = {ber}")

plt.semilogy(snr_db_list, ber_list, '.-')
plt.xlabel("SNR (dB)")
plt.ylabel("symbol error rate")
plt.title("QPSK error rate vs SNR")
plt.grid(True, which='both')
plt.savefig("d26_ber.png", dpi=120)
print("saved")