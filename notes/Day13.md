## Pulse Shaping Filter
#### ISI（Inter-Symbol-Interference, 符號間干擾）
- 透過 pulse shaping filter 壓縮 Boxcar 佔用的過多頻寬
- 傳輸 symbols 時是連續傳輸，而加上 pulse shaping filter 後會導致
	1. 時域拉長（頻域壓縮）
	2. 相鄰 symbol 重疊
- 因此 shaping filter 需符合：在該 pulse 峰值的時刻，其他 pulse 值為 0
![[pulse_train.svg]]

### Matched Filter
- Matched Filter：在 Tx 和 Rx 兩端使用相同的 filter
	1. 信號可以帶著 ISI 傳遞，只要在 receiver sampling 之前解決就好
	2. sampling 發生在 sender(Tx)'s low-pass and receiver(Rx)'s low-pass 之後
	3. 現代會將 pulse shaping filter 平均拆分到兩端
- receiver 跟相同的 filter 捲積，讓雜訊被過濾，並進一步讓波峰更清楚

#### 原理
convolution 具有**結合律**
$$(f * g) * h = f * (g * h)$$
且時域捲積=頻域相乘
$$g(t) * h(t) \leftrightarrow G(f)H(f)$$
因此，要將 filter 拆兩半，可以取其平方根
$$X(f) = X_H(f) X_H(f) \quad \mathrm{where} \quad X_H(f) = \sqrt{X(f)}$$
可以將一個 RC Filter (Raised-Cosine Filter) 拆分成兩個 Root RC Filter，等同於經過了一個RC
![[splitting_rc_filter.svg]]


#### Specific
- β（Roll-off Factor, 滾降因子 or Excess Bandwidth, 額外頻寬）：
	- 決定時域上，filter 要多快的速度衰減到 0
	- β 越小，所需 filter taps 越多，但能將頻寬降低
	- 頻寬估算公式（Rs = Symbol Rate (Hz)）$$\mathrm{BW} = R_S(\beta + 1)$$
	- β 常用 0.2~0.5 

- RC Filter（Raised-Cosine Filter）：
	- 在 β=1 時，頻域形狀是一個半週期的 cosine wave 被抬升到 x-axis 上
	- filter's pulse response（β 是唯一參數，決定在時域上衰減的速度）![[raised_cosine.svg]]
	- 衰減速度與頻域成反比![[raised_cosine_freq.svg]]
- Sinc Filter
	- equivalent to RC Filter when  β=0

#### Eye Diagrams
- 看出訊號的健康狀態（把經過 receiver's matched filter 的訊號切斷並疊圖）
- 訊號應該要在 ideal sample time 收斂到 +1, -1，中間開白區域就是 eye
![[eye_diagram.svg]]
	1. The height of the eye：amplitude margin
		- 訊號能承受多少雜訊,樣本才不會被誤判到錯誤的那一側(正負號判斷錯誤)。
		- 空隙愈大,代表訊號能承受愈強的雜訊,才會讓一個原本該讀成 +1 的樣本,被雜訊推過 0 這條線、誤判成 -1(或反過來)。
	2. The width of the eye：timing margin
		- 在理想取樣時刻附近,軌跡還維持乾淨時間範圍。
		- 範圍愈寬,代表接收端「判斷該在哪個瞬間取樣」這件事,即使跟真正的理想時刻(脈波峰值出現的那一刻)有些微偏差,讀到的值依然會落在乾淨的 +1 或 -1 附近。

- For complex modulation like QPSK or QAM, the I and Q components each carry their own symbols, so you draw a **separate eye diagram for I and for Q**, and both eyes need to be open for reliable reception.