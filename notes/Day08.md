#### 正交幅度調製（QAM, Quadrature Amplitude Modulation）
- 結合 ASK, PSK
![[Pasted image 20260831024128.png]]

- QAM 在時域中（難以區分每個 symbol 的 phase）
![[Pasted image 20260831024309.png]]

#### 頻移鍵控（FSK, Frequency Shift Keying）
- 在 N 個頻率之間切換。（每個頻率對應一個符號）
- 無法用 IQ diagram 表示（only contain Amplitude and Phase）

- 4-FSK
![[Pasted image 20260831024611.png|671]]

- FSK in time domain
![[Pasted image 20260831040155.png|671]]

- 頻譜間距（Δf）受到「symbol rate」及「pulse shaping filter」決定
	- symbol rate 越高，symbol 越短，頻寬越大


#### 差分編碼（Differential Coding）
- 發生於 Modulation 之前、Demodulation 之後
- 為了解決「相位模糊（Phase Ambiquity）」：信號通過無線信號通道會經歷隨機延遲，導致 Constellation 中發生隨機旋轉
	- 接收端同步後，將 BPSK 對齊 I-axis，但因 IQ 圖是對稱的，無法確定是否180度翻轉

##### 解法（in BPSK）
1. 導頻信號（Pilot Symbols）
	- 在信號中混入接收端已知數值的符號，反推 cluster <-> 1 or 0
	- 必須依照無線通道變化的速度，以某個週期發送
	- 會降低有效數據傳輸速率

2. 差分編碼（Differential Coding）
	- 當輸入 bit 跟「上一個==輸出==（編碼後）的 bit」相同時，輸出 0；當不同時，輸出 1。	
	- 需一個參考 bit 作為第一個 bit 輸出

- Coding
$$
y_i = y_{i-1} \oplus x_i
$$

- Decoding
$$
x_i = y_i \oplus y_{i-1}
$$


![[Pasted image 20260831041931.png|671]]
- Coding example
```
Input:     1 1 0 0 1 1 1 1 1 0
Output:  1 0 1 1 1 0 1 0 1 0 0
```


- Coding and Decoding process
![[Pasted image 20260831042600.png]]