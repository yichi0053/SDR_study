#### FFT
- FFT size: power of 2
- Cooley-Turkey Algorithm (butterfly operation)
```
import numpy as np
import matplotlib.pyplot as plt

def fft(x):
    N = len(x)
    if N == 1:
        return x
    twiddle_factors = np.exp(-2j * np.pi * np.arange(N//2) / N)
    x_even = fft(x[::2])
    x_odd = fft(x[1::2])
    return np.concatenate([x_even + twiddle_factors * x_odd,
                           x_even - twiddle_factors * x_odd])
```

#### Boxcar and Sinc
- 對 boxcar 做 FFT，會得到 sinc
- 頻譜不會在第一個低谷就停止，而是持續下去，只是起伏愈來愈小。
- 這些起伏叫 sidelobes(旁瓣)，中間那個高聳的部分叫 mainlobe(主瓣)。
- 單純的矩形之所以會產生這整套結構,原因在於它的邊緣是尖銳的：瞬間把訊號打開又關掉，需要能量分散在很廣的頻率範圍，而 sinc 正是這股能量分布的方式。
![[Pasted image 20260827082924.png]]
```
	X(f) = A·T·sinc(f·T)
```
- boxcar 與 sinc 的寬度成反比。-> windowing trade-off
- 時域上短的脈衝在頻域是寬的，時域上寬的脈衝在頻域是窄的。

