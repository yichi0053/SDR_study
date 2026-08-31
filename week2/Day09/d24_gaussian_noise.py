import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(10000)

print("mean:", np.mean(x))
print("variance:", np.var(x))

plt.hist(x, bins=50, density=True, alpha=0.7, edgecolor='black')    # histogram
plt.xlabel('value')
plt.ylabel('probability density')
plt.title('Gaussian noise histogram')
plt.savefig("d24_gaussian_noise.png", dpi=120)
print("saved")