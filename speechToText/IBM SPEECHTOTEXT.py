from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = 'PqARg8pC3RSYc1O59WuokSFue3SdSjybDXUO0xuI6LS3'
url = 'https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/79595423-893a-4d68-82bb-10534f72e136'

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator = authenticator)
stt.set_service_url(url)

import subprocess 
import os
command = 'ffmpeg -i 41agu-xa224.wav -vn -ar 44100 -ac 2 -b:a 192k audio.mp3' #41agu-xa224.wav做音檔名稱更改因檔即可
subprocess.call(command, shell=True)
command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
subprocess.call(command, shell=True)

files = []
for filename in os.listdir('.'):
    if filename.endswith(".mp3") and filename !='audio.mp3':
        files.append(filename)
files.sort()

files

results = []
for filename in files:
    with open(filename, 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel', continuous=True, \
                           inactivity_timeout=360).get_result()
        results.append(res)
        
text = []
for file in results:
    for result in file['results']:
        text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')
        
text

with open('output.txt', 'w') as out:
    out.writelines(text)        