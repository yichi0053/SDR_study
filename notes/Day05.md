### Sampling
- 在一系列特定時間區間捕捉信號值，並轉化成數字。
- sample period (T): 固定間隔時間
- sample rate (1/T): 每秒採集的樣本數

#### Nyquist Sampling (fs > 2f)
- fs / f = 1
![[Pasted image 20260829231842.png]]
- fs / f = 1.2
![[Pasted image 20260829232103.png]]
- fs / f = 1.5
![[Pasted image 20260829232111.png]]
- fs / f > 2
![[Pasted image 20260829232132.png]]

 ==fs 要夠高，才能避免捕捉到其他也吻合的信號（aliasing）==


#### Quadrature Sampling（IQ Sampling）
- 同相（I, In-Phase）-> 同相分量 cos()
- 正交（Q, Quadrature）-> 正交分量 sin()

假設發出一個訊號：signal(t) = A·cos(2πft - φ)，
但在 RF 電路中，控制振幅很簡單，控制相位卻很難，
因此可以利用恆等式：a cos(x) + b sin(x) = A cos(x - φ)，
說明可用「兩特定幅度、初始相位為0、同頻率的 cos , sin 合成特定的 cos，
再將a, b 替換為 I, Q，並帶入 x = 2.pi.f.t，可得到：
$$
\begin{aligned}
& A \cos(2\pi f t - \phi) \\
&= I \cos(2\pi f t) + Q \sin(2\pi f t)
\end{aligned}
$$
並且：
$$
\begin{aligned}
A &= \sqrt{I^2 + Q^2} \\
\phi &= \tan^{-1}\left(\frac{Q}{I}\right)
\end{aligned}
$$
==透過控制 I, Q 分量，可合成任意幅度、相位的餘弦波==


#### Complex Number
- 樣本點：I （實）+ j*Q（虛）
- 直角座標形式：z = a + jb
- 極座標形式：z = r · e^(jθ)

「相量圖（phasor diagram）」
![[Pasted image 20260829235034.png]]
- Amplitude: 線段長度
- Phase: 向量與 x 軸夾角

- FFT 還能找出==每個 frequency domain 分量對應的「正弦波形在時間上的偏移」==，所有對應的==正弦波加總起來就能還原「原本（或非常接近）的 time domain signal」==
