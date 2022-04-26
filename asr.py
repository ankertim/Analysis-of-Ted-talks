import os
import speech_recognition as sr
from video2audio import main as video2audio
from cut_audio import CutAudios

class setting(object):
    def __init__(self):
        self.video_path = 'database/video/'
        self.audio_path = 'database/audio/'
        self.cutPath = 'database/cutaudio/'
        self.Trans = 'database/Transcription/'
        self.WordCloud = 'database/wordcloud/'
        self.freq_path = 'database/wordFrequency/'
        self.video_type = '.mp4'
        self.audio_type = '.wav'

def asr(file, audio_type, cutPath, cutNum, Trans):
    AUDIO_FILE = cutPath + file 
    r = sr.Recognizer()
    a = ""
    for i in range(0, cutNum):
        with sr.WavFile(AUDIO_FILE + '-' + str(i) + audio_type) as source: #讀取wav檔
            audio = r.record(source)
        try:
            b = r.recognize_google(audio, language="en-US")
            #print("i: %d\n%s" % (i, b))
            a += ' ' + b
            #print(a)
        except LookupError:
            print("Could not understand audio")
        except Exception as e:
            print('Error[2]:', e)
    with open(Trans + file + '.txt', 'w') as File:
        File.write(a)
    #print("Transcription:", a)

def main(file, obj):
    print('file: %s' % file)
    video2audio(obj.video_path, file, obj.audio_path, obj.video_type, obj.audio_type)
    print('Cut file: %s' % obj.audio_path + file + obj.audio_type)
    cutNum = CutAudios(obj.audio_path, file, obj.audio_type, obj.cutPath)
    print('cutNum: %d' % cutNum)
    print('ASR file: %s' % obj.audio_path + file + obj.audio_type)
    asr(file, obj.audio_type, obj.cutPath, cutNum, obj.Trans)
    print('asr finish')

if __name__ == '__main__' :
    obj = setting()
    files = os.listdir(obj.video_path)
    files = [f.replace(obj.video_type, '') for f in files if f.endswith(obj.video_type)]
    files = ["減少碳排放的具體想法"]
    for file in files:
        main(file, obj)
        print()
    print('End')