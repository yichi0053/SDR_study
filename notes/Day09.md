### Noise
#### Gaussian Noise
- 高斯分佈（常態分佈）
	1. mean = 0
	2. var = σ²（決定噪音的強度）

- 多個隨機結果疊加往往近似常態
![[Pasted image 20260831173700.png]]

- Gaussian noise in frequency domain is also Gaussian noise
![[Pasted image 20260831230236.png|680]]


#### dB（Decibels）
- 對數表達形式，提供更大的動態範圍
- dB 是無單位的
- x to dB
$$
x_{\text{dB}} = 10 \log_{10} x
$$
- dB to x
$$
x = 10^{x_{dB}/10}
$$



#### Complex Noise
- 基於 baseband 的 Gaussian Noise
	1. 雜訊功率在實部、虛部上均勻分佈
	2. 實部、虛部互相獨立
![[Pasted image 20260831232807.png]]

- 生成 Gaussian Noise
```
n = np.random.randn() + 1j * np.random.randn()   # result = 2
||
||  power = np.var(x)   # x is normal distributed, variance = 1
||  Var(aK) = a² · Var(X)
\/
n = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)

# np.sprt(2)
power(n_raw / k) = (1/k)² × power(n_raw)
                 = (1/k)² × 2
                 = 2/k²
```

- 當噪聲過高，會難以分辨目標頻率
![[Pasted image 20260831232901.png]]


#### AWGN（Additive White Gaussian Noise）
- Additive：雜訊是被添加到接收信號中的
- White：頻譜在整個觀測頻帶上是平坦的（PSD 在所有頻率上恆定）


#### SNR（Signal-to-Noise Ratio, 信噪比）
- 比較信號強度合雜訊水平的差異（dB）
- recall Power = Var
$$
\text{SNR} = \frac{P_{\text{signal}}}{P_{\text{noise}}} = \frac{\sigma_{\text{signal}}^2}{\sigma_{\text{noise}}^2}
$$

- SINR（Signal-to-Interference-plus-Noise Ratio）
	- 分母加上了干擾項
$$\mathrm{SINR} = \frac{P_{signal}}{P_{interference} + P_{noise}}$$

### Random Variables
#### Joint Distribution
- Joint PDF
- X 取值 x，同時 Y 取值 y 的可能性
$$f_{X,Y}(x,y)$$
- If two variables are independent to each other
$$f_{X,Y}(x,y) = f_X(x) \cdot f_Y(y)$$
#### Probability Distribution
- PDF（Probability Density Function）
- in ND ( μ: center  , σ²: degree of discrete)
$$f_X(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$
#### Expectation
- For a continuous random variables with PDF
$$E[X] = \int_{-\infty}^{\infty} x \cdot f_X(x) \, dx$$
- Linear property
$$E[aX + b] = aE[X] + b$$
$$E[X + Y] = E[X] + E[Y]$$
#### Variance
$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$
- For a zero-mean signal, the variance is equal to the average power.
$$P = \text{Var}(X) = E[X^2] \quad \text{（当 } E[X] = 0\text{）}$$
- Variance of the sum of two variables
$$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X,Y)$$


#### Covariance
- 關聯程度
$$\text{Cov}(X,Y) = E[(X - E[X])(Y - E[Y])]$$
or
$$\text{Cov}(X,Y) = E[XY] - E[X]E[Y]$$
Cov 有單位，實務常使用 Covariance Coefficient：
$$\rho_{XY} = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$$

#### Complex Random Variables
- 最常見的就是 Complex Gaussian Noise（X, Y 是具有相同 Var 的 RV）
- If `X ~ N(α₁, σ₁²)` and `Y ~ N(α₂, σ₂²)` are independent of each other
	`Mean:     E[Z] = E[X] + jE[Y] = α₁ + jα₂`
	`Variance: Var(Z) = Var(X) + Var(Y) = σ₁² + σ₂²`

#### Random Process (a.k.a Stochastic Process)
- 一組依時間排列的隨機變數：`X(t) or X[n] (discrete time)`
- 如果特性不隨時間變化，稱為平穩（stationary），如廣義平穩（WSS）：
	1. 恆定均值：for all the t , `E[X(t)] = μ`
	2. 自相關只取決於時間差（τ）：`E[X(t)X*(t+τ)]`