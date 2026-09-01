### FIR Filter Design
#### Python
- `scipy.signal.firwin`，需要指定：
	1. the number of Filter Taps
	2. the cutoff
	3. (fs)
```
from scipy.signal import firwin
sample_rate = 1e6
h = firwin(101, [100e3, 200e3], pass_zero=False, fs=sample_rate)
print(h)
```

- `scipy.signal.firwin2`，更加靈活，可指定多個頻率及增益
	1. the number of Filter Taps
	2. (fs)
```
from scipy.signal import firwin2
sample_rate = 1e6
freqs = [0, 100e3, 110e3, 190e3, 200e3, 300e3, 310e3, 500e3]
gains = [1, 1,     0,     0,     0.5,   0.5,   0,     0]
h2 = firwin2(101, freqs, gains, fs=sample_rate)
print(h2)
```

- other options (all involve performing a convolution operation)
	1. `np.convolve`
	2. `scipy.signal.convolve`
	3. `scipy.signal.fftconvolve`
	4. `scipy.signal.lfilter`
```
import numpy as np
from scipy.signal import firwin2, convolve, fftconvolve, lfilter

# Create a test signal, we'll use Gaussian noise
sample_rate = 1e6 # Hz
N = 1000 # samples to simulate
x = np.random.randn(N) + 1j * np.random.randn(N)

# Create an FIR filter, same one as 2nd example above
freqs = [0, 100e3, 110e3, 190e3, 200e3, 300e3, 310e3, 500e3]
gains = [1, 1,     0,     0,     0.5,   0.5,   0,     0]
h2 = firwin2(101, freqs, gains, fs=sample_rate)

# Apply filter using the four different methods
x_numpy = np.convolve(h2, x)
x_scipy = convolve(h2, x) # scipys convolve
x_fft_convolve = fftconvolve(h2, x)
x_lfilter = lfilter(h2, 1, x) # 2nd arg is always 1 for FIR filters

# Prove they are all giving the same output
print(x_numpy[0:2])
print(x_scipy[0:2])
print(x_fft_convolve[0:2])
print(x_lfilter[0:2])
```

- `scipy.signal.fftconvolve` has better performance
![[convolve_comparison_1000.svg|409]]

![[convolve_comparison_100000.svg|415]]


#### Stateful Filtering
- `lfilter_zi` in SciPy
- 可儲存上次呼叫濾波器的輸出作為這次輸入的初始條件（面對連續資料流的情況）
```
b = taps
a = 1 # for FIR, but non-1 for IIR
zi = lfilter_zi(b, a) # calc initial conditions
while True:
    samples = sdr.read_samples(num_samples) # Replace with your SDR's receive samples function
    samples_filtered, zi = lfilter(b, a, samples, zi=zi) # apply filter
```


### Arbitrary Frequency Response
- Design an FIR filter myself in Python
	1. Step1: Design my desired frequency domain response
![[Pasted image 20260901123950.png]]
	2. Step2: Converts the frequency response with IFFT
![[Pasted image 20260901124241.png|680]]
	3. Step3: Verify by taking FFT of  taps
![[Pasted image 20260901124523.png]]
	4. Step4: Fix the decay problem
		1. Window the impulse response
		2. Interpolate (add more resolution to the desired response)