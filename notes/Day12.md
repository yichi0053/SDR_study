數字基帶信號是一串 complex number：
	`[I+jQ, I+jQ, I+jQ...]`
	儲存時會使用以下格式：
	`IQIQIQIQIQ....`
	讀取時要再將其分離成`[I+jQ, I+jQ, I+jQ...]`的形式
	通常用 Binary Files 存儲，節省空間

- **Python**： Complex number default  to `np.complex128`(2 * `float64`). But in DSP/SDR, we tend to use `int16 or float32`(ADC in SDR simply do not have that level of precision)

- 從 SDR 設備接收 samples 時，要先了解最大值（某些設備默認為 1.0，某些使用整數形式，因此會是 +32767, -32768），若是信號超過接受器最大值，將會飽和（Saturate），信號被截斷
![[Pasted image 20260902154426.png]]


- SigMF（針對信號紀錄的 metadata 的開放標準）
	- IQ 文件本身不包含 metadata（常見作法為透過新增第二個文件，包含信號的 sample rate， SDR 設備的接收中心頻率等等），現可使用 SigMF 開放標準：
		1. 將 `.iq` 重新命名為 `.sigmf-data`
		2. 新增文件 `.sigmf-meta`：
```
{
    "global": {
        "core:datatype": "cf32_le",   # float32
        "core:sample_rate": 1000000,
        "core:hw": "PlutoSDR with 915 MHz whip antenna",
        "core:author": "Art Vandelay",
        "core:version": "1.0.0"
    },
    "captures": [
        {
            "core:sample_start": 0,
            "core:frequency": 915000000
        }
    ],
    "annotations": []
}
```


#### 分析 IQ files steps
1. **讀檔**  
	`np.fromfile` 明確指定 dtype,否則預設當 float64 讀,資料全亂。
	int16 等無原生複數型別要用 `raw[::2]+1j*raw[1::2]` 交錯重組。
2. **檢查飽和**  
	看 `max(abs(samples))` 是否卡在型別理論上限。
	飽和會讓頻域出現假的擴散特徵,須在分析前排除。
3. **算 PSD**  
	六步驟(FFT→abs→平方→除以N·Fs→10log10→fftshift)。
	陌生檔案訊號強度未知,線性刻度容易讓弱訊號消失,一定要轉 dB。
4. **找訊號位置**  
	用 `argmax` 自動抓峰值。若峰值精確落在 0 Hz 且異常尖窄,先懷疑是 DC spike(LO 洩漏)而非真訊號。
5. **搬移到 baseband**  
	乘上 `exp(-j2π·peak_freq·t)`,把偵測到的訊號位置搬到 0 Hz,方便後續濾波與觀察。
6. **濾波+降取樣**  
	必須先濾波才能降取樣,否則混疊。濾波器同時扮演通道選擇與抗混疊兩種角色。
7. **看星座圖判斷調變**  
	2 群→BPSK;
	4 群均勻分布→QPSK;
	分布在不同半徑→QAM;
	只有一團模糊圓→可能是 FSK,改看 spectrogram。
