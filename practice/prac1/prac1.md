### 程式實作題
題目:分析一份下載回來的陌生 IQ 檔案

###情境設定
你已經從上面任一來源下載了一個 .iq(或 .sigmf-data)檔案。假設檔名是 mystery_capture.iq,你只知道取樣率(從 meta 檔或檔名得知,例如 2,000,000 Hz),完全不知道:

裡面有沒有真的訊號,還是只有雜訊
如果有訊號,它在哪個頻率
訊號是哪種調變方式
資料有沒有飽和

### 你要做的事
依你上次整理的七步驟流程,寫一支程式,對這份檔案做完整分析,並且最後用文字印出你的結論(不是只有畫圖,要能像寫報告一樣講出「我認為這份錄音裡有沒有訊號、大約在什麼頻率、可能是什麼調變」)。

### 具體要求
讀檔:用正確的方式讀入,若不確定型別,依 Day 12 學到的預設假設處理,並在程式裡註解說明你的假設依據
飽和檢查:印出最大振幅,並寫一行判斷邏輯,自動印出「疑似飽和」或「正常」
PSD 分析:畫出來,並且自動列出所有明顯高於雜訊地板的頻率位置(不只抓最大值一個,因為可能不只一個訊號)——這裡需要你自己設計一個合理的「門檻」判斷邏輯
DC spike 排除:你的偵測邏輯必須能分辨「0 Hz 那根尖峰是不是 DC spike」,不要傻傻地把它當成真訊號報告出去
針對偵測到的每一個訊號,各自搬移到 baseband,畫出星座圖
自動判讀:寫一個簡單的判斷函式,依星座圖的群集特徵(可以用 magnitude 跟 phase 的分布去寫判斷式,不需要多複雜),猜測是哪一種調變,並印出信心程度(例如「群集數量不明顯,可能是 FSK 或雜訊,建議改看 spectrogram」)

最後印出一段結論摘要,像這樣的格式:
=== Analysis Report: mystery_capture.iq ===
Sample rate: 2,000,000 Hz
Saturation check: PASS (max |sample| = 1.08)
Detected signals: 1
  Signal 1: center freq ≈ 340,210 Hz, estimated modulation: QPSK (4 clusters found)
DC spike detected at 0 Hz: YES (excluded from signal list)
