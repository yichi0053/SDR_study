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

### Day 8｜Ch4 後半:FSK、差分編碼、QPSK 模擬

**閱讀**:PySDR Ch4 Frequency Shift Keying、Differential Coding、Python Example

**實作**

- `d21_qpsk_symbols.py`:產生 QPSK 符號(`x_int` → 角度 → 弧度 → `cos+1j*sin`),
- `d22_noise.py`:加入 AWGN,觀察星座點擴散;另做 phase noise 對照
- `d23_differential.py`:實作差分編碼與解碼


---

### Day 9｜Ch10 Noise and Random Variables

**閱讀**:PySDR Ch10 全章(Gaussian Noise、隨機變數、SNR、SINR、AWGN 完整定義)

**實作**

- `d24_gaussian_noise.py`:產生高斯雜訊,畫出直方圖(histogram)驗證常態分布,計算變異數與功率的關係
- `d25_snr.py`:實作 SNR 計算,產生不同 SNR 下的訊號,用 PSD(Day 6 學過的六步驟)觀察雜訊地板(noise floor)的變化
- `d26_ber.py`:對 QPSK 符號掃描不同 SNR,用象限判決還原位元,統計錯誤率,畫出經驗 BER 曲線


---

### Day 10｜Ch11 Filters 前半:基礎概念與卷積

**閱讀**:PySDR Ch11 Filter Basics、Filter Representation(含 Example Use-Case、Real vs Complex Filters)、Convolution、Filter Implementation(含 FIR vs IIR)

**實作**

- `d27_convolution_demo.py`:用 `np.convolve` 實作卷積,分別對兩個方波、方波與三角波做卷積,視覺化「滑動積分」的過程,驗證輸出長度為 `N+M-1`
- `d28_moving_average.py`:實作原文提到的移動平均濾波器(taps 全為 1),對含雜訊訊號套用,用 FFT 驗證它確實是一個低通濾波器

---

### Day 11｜Ch11 Filters 後半:FIR 設計與脈波整形

**閱讀**:PySDR Ch11 FIR Filter Design(Within Python、Stateful Filtering)、Arbitrary Frequency Response、Intro to Pulse Shaping

**實作**

- `d29_firwin_design.py`:用 `scipy.signal.firwin` 設計低通濾波器,畫出 impulse response(taps)與 frequency response,比較不同 `num_taps` 與 transition width 的效果
- `d30_filter_apply.py`:用 `fftconvolve` 對含干擾的訊號套用濾波器,比較濾波前後的 PSD,驗證干擾訊號被壓到雜訊地板以下(重現原文的 Example Use-Case 情境)

---

### Day 12｜Ch14 IQ Files and SigMF:真實資料處理

**閱讀**:PySDR Ch14 全章(IQ 檔案格式、資料型別、SigMF 標準)

**實作**

- `d31_load_iq.py`:讀入公開 IQ 檔案,處理 int8/int16/float32 等不同資料型別的轉換與正規化,印出檔案基本資訊
- `d32_analyze_iq.py`:對這份陌生 IQ 資料做完整分析,套用 PSD 六步驟(Day 6)、spectrogram(Day 4)、必要時用 FIR 濾波器(Day 11)做前處理,標出可見訊號的頻率位置與大致頻寬

---

### Day 13｜Ch16 Pulse Shaping

**閱讀**:PySDR Ch16 全章

**實作**

- `d33_pulse_shaping.py`:對 QPSK 符號套用 raised-cosine 濾波器,比較整形前後的時域波形與頻譜佔用
- `d34_rolloff_compare.py`:掃描不同 β(roll-off factor)值,驗證原文提到的「β 愈小頻寬愈窄、但時域衰減愈慢」這個取捨

---

### Day 14｜Ch24 Detection using Correlation

**閱讀**:PySDR Ch24 全章

**實作**

- `d35_correlation.py`:用 `np.correlate` 實作相關偵測,在含雜訊訊號中找出已知波形的出現位置
- `d36_detection_threshold.py`:掃描不同 SNR,統計偵測率(Pd)與誤警率(Pfa),討論門檻設定的取捨