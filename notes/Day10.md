## Filter
- 主要用途
	1. 分離合併的信號
	2. 恢復失真的信號
	3. 去除雜訊
- 基本類型
	- passband：允許通過的頻率範圍
	- stopband：阻斷的頻率範圍
	1. 低通（Low-Pass）：允許低頻
	2. 高通（High-Pass）：允許高頻
	3. 帶通（Band-Pass）：允許特定範圍
	4. 帶阻（Band-Stop）：阻擋特定範圍
![[Pasted image 20260901094327.png]]


- 設立截止頻率（Cutoff Frequency）
![[Pasted image 20260901095422.png]]
- 大多數頻率為對稱
- - 中間區域為 passband
![[Pasted image 20260901095456.png|680]]
- 應用 filter 之後，得到（雜訊大幅下降）
![[Pasted image 20260901095620.png|680]]


- Transition Width（filter 在 passband 和 stopband 間切換的速度）
![[Pasted image 20260901095852.png|680]]



### Convolution
- 結合兩信號（將一個信號滑過另一個信號，同時作積分）
- 輸出長度大於輸入長度（N + M - 1）
$$(f * g)(t) = \int f(\tau) g(t - \tau) d\tau$$

### Digital Filter
#### FIR（Finite Impulse Response, 有限脈衝響應）
- 拿 Filter's Impulse Response (Filter Taps) 跟 Input 作 Convolution
	1. 以浮點數組表示，稱為 Filter Taps (h)
	2. 對於在頻域上對稱的濾波器,這些浮點數會是**實數**，且常為奇數個
	3. 較容易設計，但效率較 IIR 差
![[Pasted image 20260901105340.png]]

- IIR（Infinite Impulse Response, 無線脈衝響應）