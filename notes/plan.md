#### 執行原則

1. 每日約 3 小時（閱讀 1 小時、實作 2 小時），依你的實際可支配時間調整
2. **所有程式碼必須自己敲，可參考範例但不可整段複製**
3. 每日結束時將程式碼推上 GitHub，並在 Obsidian 記錄一則筆記
4. 遇到不懂的英文術語，查 JYW 教材取中文對照，記入術語表

#### 學習資源
1. https://blog.miniasp.com/post/2025/03/04/Understanding-WAV-format-and-PCM-encoding
2. https://pysdr.org
3. https://www.jywglady.org/sdr/contents/preface/

#### 環境準備（Day 0，約 1 小時）

bash

```bash
mkdir sdr-study && cd sdr-study
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy matplotlib
git init
```

建立目錄結構：

```
sdr-study/
├── week1/
├── week2/
├── notes/
│   └── glossary.md    # 中英術語對照表
└── README.md
```

---

### 第一週：實數訊號與頻域

#### Day 1｜取樣與時域

**閱讀**：PySDR Ch1 Introduction、Ch2 開頭至頻域介紹

**實作**

- `d01_sine.py`：產生 1 kHz 正弦波，取樣率 48 kHz，時長 0.01 秒，畫時域圖
- `d02_undersample.py`：同訊號改用 1.5 kHz 取樣，比較兩圖差異

---

#### Day 2｜FFT 與加窗

**閱讀**：PySDR Ch2 傅立葉轉換、FFT、加窗（Windowing）段落

此章以 Python 範例涵蓋傅立葉級數、傅立葉轉換、傅立葉性質、FFT、加窗與頻譜圖。 [PySDR](https://pysdr.org/content/frequency_domain)

**實作**

- `d03_fft_basic.py`：對 Day 1 訊號做 FFT，正確標註頻率軸，驗證峰值在 1 kHz
- `d04_fft_multi.py`：疊加 1 kHz、3 kHz、7 kHz 三個正弦波，用 FFT 分離
- `d05_window.py`：對非整數週期訊號，比較無窗與 Hamming 窗的 Spectral Leakage
---

#### Day 3｜混疊與抗混疊濾波

**閱讀**:PySDR Ch2 剩餘部分
**補充查閱** Aliasing 相關段落(PySDR Ch3 IQ Sampling 開頭的 Nyquist Sampling 小節有概念性說明,但無數值折疊公式與濾波器程式碼,需額外補充通用 DSP 知識)

**實作**

- `d06_alias_demo.py`:7 kHz 訊號用 10 kHz 取樣,FFT 觀察峰值出現位置
- `d07_alias_calc.py`:寫函式 `predict_alias(f_signal, f_sample)` 預測混疊頻率,並用多組數值驗證
- `d08_antialias.py`:加入 `scipy.signal` 低通濾波後重做 Day 6,驗證濾波器作用


---

### Day 4｜與 WAV 實檔接軌

**閱讀**:重讀保哥 WAV/PCM 文章

**實作**

- `d12_wav_inspect.py`:讀 WAV,印出取樣率、聲道數、資料型別
- `d13_wav_verify.py`:理論檔案大小 vs `os.path.getsize()`,驗證 44 bytes 差額
- `d14_wav_spectrogram.py`:對真實錄音畫頻譜圖

---

### Day 5–6｜Ch3 IQ Sampling

#### Day 5:量化基礎與複數 FFT

**閱讀**:PySDR Ch3 Sampling Basics、Nyquist Sampling(複習)、Quadrature Sampling、Complex Numbers、Complex Numbers in FFTs

**實作**

- `d15_complex_signal.py`:用 `numpy.complex64` 產生複數指數訊號,畫 I/Q 路
- `d16_iq_plane.py`:IQ 平面軌跡
- `d17_complex_fft.py`:對複數訊號做 FFT,觀察負頻率不對稱

#### Day 6:下變頻與功率譜密度

**閱讀**:PySDR Ch3 Receiver Side、Carrier and Downconversion、Receiver Architectures、Baseband and Bandpass Signals、DC Spike and Offset Tuning、Calculating Average Power、Calculating Power Spectral Density

**實作**

- `d18_bandwidth.py`:驗證複數取樣有效頻寬等於取樣率
- `d18b_psd.py`:依原書六步驟計算 PSD,嘗試 DC spike 的模擬與觀察

---

### Day 7–8｜Ch4 Digital Modulation

#### Day 7:調變與星座圖

**閱讀**:PySDR Ch4 前半(ASK、PSK、QAM、FSK、星座圖)

**實作**

- `d19_bpsk_mod.py`:自行實作 BPSK 調變
- `d20_constellation.py`:畫星座圖

#### Day 8:解調與錯誤率

**閱讀**:PySDR Ch4 後半

**實作**

- `d21_bpsk_demod.py`:BPSK 解調,驗證位元正確還原
- `d22_noise.py`:加入 AWGN,觀察星座點擴散
- `d23_ber.py`:不同 SNR 下的 BER 曲線

---

### Day 9–10｜Filters 章節

#### Day 9:FIR 濾波器設計

**閱讀**:PySDR Filters 章節前半(FIR、頻率響應、convolution 實作面)

**實作**

- `d24_fir_filter.py`:設計 FIR 低通濾波器,畫頻率響應

#### Day 10:降採樣與抗混疊銜接

**閱讀**:PySDR Filters 章節後半(Decimation)

**實作**

- `d25_decimation.py`:高取樣率訊號抽取,比較有無前置濾波的差異,呼應 Day 3 抗混疊概念

---

### Day 11–12｜真實 IQ 資料驗收

#### Day 11:讀取與檢視

**閱讀**:搜尋 SigMF sample recordings 或公開 RTL-SDR IQ 錄音,閱讀資料格式說明

**實作**

- `d26_load_iq.py`:讀入陌生 IQ 檔,處理 int8/int16/float32 等不同資料型別

#### Day 12:完整分析

**實作**

- `d27_analyze_iq.py`:畫頻譜圖,標出可見訊號的頻率位置與大致頻寬,套用 PSD 六步驟與 Day 10 學到的濾波技巧做前處理

---

### Day 13｜整理與回報

**產出三份文件**

1. GitHub repo README:說明每支程式的用途與執行方式
2. 技術筆記:每個核心概念的中文摘要,附圖表
3. 未解問題清單:條列尚未理解的部分,作為下次向教授請教的議題清單