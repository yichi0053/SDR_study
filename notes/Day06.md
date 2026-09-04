### Receiver
- Receiver side：透過兩個 ADC 對 I, Q 分別採樣，並以複數儲存。
![[Pasted image 20260830155027.png]]
1. Input Signal ： `I(t)·cos(2πft) + Q(t)·sin(2πft)`
2. LO（Local Oscillator, 本地振盪器）（⊙ with sine wave）：產生一個固定頻率的正弦波,頻率設定跟載波 f 相同。
3. 90° Shifter：將 LO 產生的正弦波偏移 90° 相位，產生餘弦波。
4. Mixer ( ⊗ )：將 Input 乘上 cos, sin 輸出 I, Q。 

#### Architectures
- Direct Sampling (Direct RF)：直接以足夠快的 fs 採樣
- Direct Conversion (Zero IF)：將輸入 downconverse（to baseband） 並分解為 I, Q
- Superheterodyne：舊型收音機架構
- LNA (Low-Noise Amplifier)：適用於極低功率輸出的放大器
![[Pasted image 20260830163349.png]]


#### Carrier
- f（carrier）：發送信號的中心頻率，承載要發送的信號。
- carrier waveform：cos(2πft), sin(2πft)


#### Downconversion
- 將 carrier frequency 降至以 0Hz 為中心
	1. 透過「frequency shift property」：`x(t)·e^(j2πf₀t)  ↔  X(f - f₀)`
	2. 不是直接將 f 設為 0
![[Pasted image 20260830163213.png]]



- Baseband（基頻， 複數）：訊號中心頻率位在 0 Hz 附近的狀態。
- Bandpass（帶通，實數）：訊號存在於某個遠離 0 Hz 的射頻頻率上,是為了無線傳輸而被搬移上去的狀態。
![[Pasted image 20260830164851.png]]
==正負頻率不對稱一定是「複數」==
（若信號完全沒有虛數Q，訊號只剩下沒有位移的 cos，疊加起來沿  y 軸對稱）


#### DC 尖峰（DC Spike）（or LO Leakage）
- Direct Conversion 中，LO 在進行 Downconversion 時，LO 本身的訊號會有部份洩漏到 Downconversion 結果的帶寬中心
- 如果整張頻譜只有中間那根尖峰、其餘部分看起來都像雜訊，那很可能代表這個位置其實沒有真正的訊號，只是一個假訊號。
![[Pasted image 20260830165428.png]]
- 解決：Offset Tuning

#### Offset Tuning
- 將頻率中心遠離，並提高 sampling rate
![[Pasted image 20260830170047.png]]


#### Calculate
- Average Power：
```
P = (1/N) · Σ |x[n]|² 

# Python
avg_pwr = np.mean(np.abs(x)**2)

# if μ approach to 0
avg_pwr = np.var(x)     ->    P = (1/N) · Σ |x[n] - μ|² 
```

- PSD (Power Spectral Density)：
	- FFT 輸出的結果就是 PSD（將頻域可視化）
	- 得出 PSD 步驟：
		1. **取 FFT**：對樣本做 FFT,若輸入長度是 N,FFT 輸出也是長度 N 的複數陣列
		2. **取絕對值(magnitude)**：把複數陣列轉成實數
		3. **平方**：把 magnitude 平方,轉換成 power(功率)
		4. **正規化**：除以 FFT 長度 N,再除以取樣率 Fs
		5. **轉成 dB**：用 `10·log10()`,PSD 慣例上永遠用對數刻度呈現
		6. **做 fftshift**：把 0 Hz 移到中間、負頻率移到左半邊
