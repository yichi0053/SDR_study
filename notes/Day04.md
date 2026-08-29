## [理解 WAV 格式：從 PCM 編碼格式到檔案大小計算方法](https://blog.miniasp.com/post/2025/03/04/Understanding-WAV-format-and-PCM-encoding)

### WAV (Waveform Audio File Format, 波形音頻檔案格式)
- 儲存未壓縮的音頻數據
- 基於 RIFF 的應用
```
WAV 三層結構：

RIFF chunk(最外層容器)
├── "RIFF" (4 bytes)          ← 檔案識別碼
├── ChunkSize (4 bytes)        ← 整個檔案大小
├── "WAVE" (4 bytes)           ← 說明這是 WAVE 格式
├── fmt subchunk(格式資訊)
│   ├── "fmt " (4 bytes)
│   ├── Subchunk1Size (4 bytes)
│   ├── AudioFormat (2 bytes)      ← 1 代表 PCM(未壓縮)
│   ├── NumChannels (2 bytes)      ← 聲道數
│   ├── SampleRate (4 bytes)       ← 取樣率,對應你這幾天的 fs
│   ├── ByteRate (4 bytes)         ← 每秒位元組數
│   ├── BlockAlign (2 bytes)       ← 每個取樣點佔幾個 byte
│   └── BitsPerSample (2 bytes)    ← 位元深度
└── data subchunk(實際音訊資料)
    ├── "data" (4 bytes)
    ├── Subchunk2Size (4 bytes)    ← 實際 PCM 資料的長度
    └── 實際的 PCM 樣本資料...
    
檔案總大小 = header (44 Bytes) + 
			PCM data（資料大小 = 樣本數 × 聲道數 × 樣本 byte 數 × t）
```

- 優點
	- 未壓縮：保持原始音質（適合專業錄音、編輯）
	- 廣泛兼容：幾乎所有音頻軟硬體都支援
	- 適合長期檔案保存
- 缺點
	- 檔案大：儲存、傳輸成本高
	- 不適合 stream 或 網上分享，尤其是長時錄音
- 常見用途
	- 音樂製作和音效編輯（高品質音頻）
	- 音頻檔案保存
	- 遊戲音效和廣播（需高保真率）

#### WAV
- 位元深度（bit depth）
	- 儲存音頻樣本使用的位數
	- 量化的精細程度由此決定
- 取樣率（sampling rate）
	- 每秒鐘對連續訊號取樣的次數（fs, Hz）
	- recall Nyquist Theorem：fs > f * 2
- 聲道數（channels）
	- 單一檔案中儲存的音頻數量（1-mono, 2-stereo）
```
WAV 中 multi-channel 的排列方式：interleaved(交錯儲存)

[左聲道樣本1][右聲道樣本1][左聲道樣本2][右聲道樣本2]...
   2 bytes      2 bytes      2 bytes      2 bytes
```
	- SDR use IQ sampling（I-left, Q-right）

- 檔案大小（Bytes）=（Sampling Rate * Bit Depth * channels * t）/ 8


#### RIFF (Resource Interchange File Format, 資源交換檔案格式)
- 用於多媒體資料的檔案格式
- 由一系列稱為「區塊（chunk）」的資料結構組成：
```
chunk固定包含三個部份：

chunk ID(4 bytes,例如 "RIFF"、"fmt "、"data")
chunk size(4 bytes,這個 chunk 的資料長度,不含 ID 和 size 本身)
chunk data(實際內容,長度就是上面那個 size 講的)
```

#### PCM (Pulse Code Modulation, 脈衝編碼調變)
- 將「音頻訊號 analog」轉為「數位資料 digital」的方法
- WAV 中常見的編碼方式，保留音頻的原始品質

- 基本工作原理
	1. 取樣（Sampling）
		- 對連續的類比訊號依固定時間間隔取樣，得到一系列離散數據點
	2. 量化（Quantization）
		- 將取樣的數據點轉為有限數量的離散值（通常是將訊號幅度分為若干級別）
	3. 編碼（Encoding）
		- 將量化後的離散值轉換為二進制數據，形成數位訊號


### Spectrogram(頻譜圖)

#### 為什麼需要它

- FFT 只能回答「整段時間裡有哪些頻率」,無法回答「何時發生」

#### 運作原理

- 把長訊號切成多個(可重疊的)小段,每段各自做一次 FFT,依時間排列成二維圖(橫軸時間、縱軸頻率、顏色代表能量)
- `nperseg`:每段的樣本數,決定分析的頻率解析度(`fs/nperseg`)與時間解析度(`nperseg/fs`)
- `noverlap`:相鄰段的重疊樣本數,讓時間軸更平滑

#### Time-Frequency Tradeoff(時頻取捨)

- `nperseg` 愈小 → 時間解析度愈細(能分辨快速變化)、頻率解析度愈粗(相近頻率會糊在一起)
- `nperseg` 愈大 → 頻率解析度愈細、時間解析度愈粗(細節被平均掉)
- 本質是同一個參數同時控制兩個互斥的東西,不可能兩者同時最佳化