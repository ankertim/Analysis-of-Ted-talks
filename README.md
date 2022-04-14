# TED 英文演講語音分析器

Demo: https://youtu.be/YfwkKQrnxyo

## 研究動機

因應現代人生活繁忙，有時候想看一些英文演講，卻又沒有時間完整的觀看。所以我們做了一個英文演講分析器，幫忙分析出英文演講的重點，讓使用者可以在短時間了解演講的概要，方便之後有時間完整聆聽時可以迅速理解演講的重點。

## 研究目的

架設一個網站，讓使用者可輸入 TED 英文演講網址，系統再對此演講進行分析，產生出該演講的文字雲，幫助使用者了解演講內容。

## 研究方法

### 爬蟲
- 使用套件：requests, bs4, re, string
- 因 TED 網站有提供使用者下載影片的功能，我們利用爬蟲，以及正規表示式，篩選出下載網址來下載影片。

### 影片轉音檔
  - 使用套件：moviepy
  - 將 mp4 轉成 wav 的音檔
  - **分割音檔:**
  - 使用套件：wave, numpy, pylab, librosa
  - 將音檔用 12s 來分割成數個音檔

### 語音辨識
- 使用套件：speech_recognition
- 利用 google web speech api 對音檔進行語音辨識。
- ![](https://i.imgur.com/RIMiWy1.png)


### 文字分析
- **前處理:**
- 使用套件：nltk(Nature Language Tool Kit), panda
- 使用nltk.word_tokenize() 進行斷詞
- 去除停用詞
- ![](https://i.imgur.com/Aa7qZ61.png)
- **文字雲:**
- 使用套件：wordcloud, imageio
- 可對要製作的文字雲做一些設定，如： 文字雲的形狀、背景顏色。
- ![](https://i.imgur.com/w9d8aMR.jpg)
- **統計字詞出現的頻率:**
- ![](https://i.imgur.com/Gu15Jwy.png)


### 架設網站
- 使用套件：flask
- 使用python flask 架設 web server，後端對語音辨識、文字分析等功能進行整合，再跟前端串聯。

