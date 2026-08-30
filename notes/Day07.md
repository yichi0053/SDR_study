#### Symbols
- 攜帶特定大小的訊息
- 傳輸速度越快，帶寬越大（時域變化越快,頻域佔用越寬）

- IEEE 802.3（1 symbol 2 bits）
![[ethernet 1.svg]]


#### Wireless Symbols
- 為何不能直接在無線通信系統中傳輸乙太網路信號？
	1. 天線尺寸：通常設計成波長的1/2, 1/4，`λ=c/f`頻率越低，波長越長，天線越長，且訊號包含 0 Hz，理論尺寸就趨近無限。
	2. 方波信號：「時域上變化越大，頻域中佔用頻寬越大」，方波的變化大。
![[Pasted image 20260830215433.png]]
==改用 Carrier 傳輸==

### Carrier Modulation
	1. Amplitude
	2. Phase
	3. Frequency

#### 幅移鍵控（ASK, Amplitude Shift Keying）==Amplitude==
- 將 symbol（含 N 個樣本點）乘上一個正弦波
![[Pasted image 20260830233404.png]]

- example
![[Pasted image 20260831004512.png]]

#### 相移鍵控（PSK, Phase Shift Keying）==Phase==
- 二進制相移鍵控（BPSK）
	1. 無相位改變（0 度）
	2. 相位反轉（180 度）
![[Pasted image 20260831001508.png|671]]

- example
![[Pasted image 20260831004434.png]]

#### 頻移鍵控（FSK, Frequency Shift Keying）==Frequency==


#### 星座圖（Constellation）
- 星座圖畫的是 baseband 的符號位置（complex），不含 carrier