import os
import wave
import numpy as np
import pylab as plt
import math
import librosa

def CutAudios(path, file, audio_type, cut_path):
    CutTime = 20 #單位長度20s
    FileType = path + file + audio_type
    f = wave.open(FileType, 'rb')
    params = f.getparams() #讀取音訊檔案資訊
    nchannels, sampwidth, framerate, nframes = params[:4] #聲道數,量化位數,取樣頻率,取樣點數  
    str_data = f.readframes(nframes)
    f.close()

    wave_data = np.frombuffer(str_data, dtype=np.short)
    #根據聲道數對音訊進行轉換
    if nchannels > 1:
        wave_data.shape = -1,2
        wave_data = wave_data.T
        temp_data = wave_data.T
    else:
        wave_data = wave_data.T
        temp_data = wave_data.T

    CutFrameNum = framerate * CutTime 
    cutNum = math.ceil(nframes/CutFrameNum) #音訊片段數
    StepNum = int(CutFrameNum)
    StepTotalNum = 0

    for j in range(cutNum):
        FileType = cut_path + file + "-" + str(j) + audio_type
        temp_dataTemp = temp_data[StepNum * (j):StepNum * (j + 1)]
        StepTotalNum = (j + 1) * StepNum
        temp_dataTemp.shape = 1,-1
        temp_dataTemp = temp_dataTemp.astype(np.short)# 開啟WAV文件
        f = wave.open(FileType, 'wb')
        # 配置聲道數、量化位數和取樣頻率
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(temp_dataTemp.tostring()) # 將wav_data轉換為二進位制資料寫入檔案
        f.close()
    return cutNum