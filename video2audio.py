from moviepy.editor import *

def main(video_path, file, audio_path, video_type, audio_type):
    # ex: audioType = '.wav'
    video = VideoFileClip(video_path + file + video_type)
    audio = video.audio
    #audio.write_audiofile('test.wav')
    audio.write_audiofile(audio_path + file + audio_type)

if __name__ == '__main__':
    path = 'C:\\Users\\yen\\Downloads\\大學課程\大四課程(下)\\敏捷開發\\project\\database\\video\\'
    audioPath = 'C:\\Users\\yen\\Downloads\\大學課程\大四課程(下)\\敏捷開發\\project\\database\\audio\\'
    