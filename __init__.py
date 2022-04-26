import sys
from flask import Flask, jsonify, request, render_template, redirect, url_for, send_from_directory, Blueprint
import os
from asr import main as asr
from WordCloud_proj.Analysis import main as analysis
from downloadVideo import videoDownload

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

# global variable
video_name = None
mask = None
obj = setting()

database = Blueprint('db', __name__, static_folder='database/')
app = Flask(__name__, static_folder='web/static/', template_folder='web/templates/')
app.register_blueprint(database)

@app.route('/')
def index():
    global video_name, mask
    if video_name != None:
        wordcloud = url_for('db.static', filename = 'wordcloud/' + video_name + '_' + mask + '.jpg', video_name = video_name)
    else:
        wordcloud = None
    return render_template('start.html', wordcloud = wordcloud, img_type = mask, video_name = video_name)

@app.route('/action', methods=['POST'])
def action():
    global video_name, obj, mask
    video_name = None
    url = request.form.get("video_url")
    mask = 'circle' # default
    print(url, mask)
    video_name = videoDownload(url, obj.video_path)
    if video_name == 1:
        result = """
            <script type="text/javascript">
                window.alert('無法抓到網頁');
                window.history.back(-1);
            </script> 
            """
        video_name = None
        return result
    elif video_name == 2:
        result = """
            <script type="text/javascript">
                window.alert('無法下載影片');
                window.history.back(-1);
            </script>
            """
        video_name = None
        return result
    asr(video_name, obj)
    analysis(video_name, obj.Trans, obj.WordCloud, obj.freq_path)
    wordcloud = url_for('db.static', filename = 'wordcloud/' + video_name + '_' + mask + '.jpg')
    return render_template('start.html', wordcloud = wordcloud, img_type = mask, video_name = video_name)

@app.route('/change_mask', methods=['POST'])
def change_mask():
    global video_name, obj, mask
    mask = request.form.get("mask")
    if mask == 'unselect':
        result = """
            <script type="text/javascript"> 
                window.alert('Error');
                window.history.back(-1);
            </script> 
            """
        return result
    wordcloud = url_for('db.static', filename = 'wordcloud/' + video_name + '_' + mask + '.jpg', video_name = video_name)
    return render_template('start.html', wordcloud = wordcloud, img_type = mask, video_name = video_name)

@app.route('/download_img', methods=['POST'])
def download_img():
    global video_name, obj, mask
    if video_name == None:
        result = """
            <script type="text/javascript"> 
                window.alert('Error');
                window.history.back(-1);
            </script> 
            """
        return result
    dirpath = os.path.join(app.root_path, './database/wordcloud')
    print(dirpath)
    return send_from_directory(dirpath, video_name + '_' + mask +'.jpg', as_attachment=True)

@app.route('/download_csv', methods=['POST'])
def download_csv():
    global video_name, obj
    if video_name == None:
        result = """
            <script type="text/javascript"> 
                window.alert('Error');
                window.history.back(-1);
            </script> 
            """
        return result
    dirpath = os.path.join(app.root_path, './database/wordFrequency')
    print(dirpath)
    return send_from_directory(dirpath, video_name +'.csv', as_attachment=True)

@app.route('/history')
def history():
    path = 'web/static/data/example/'
    files = os.listdir(path)
    filetype = '.txt'
    files = [f for f in files if f.endswith(filetype)]
    content = list()
    for f in files:
        video_name = f.replace(filetype, '')
        with open(path + f, 'r') as file:
            video_url = file.read()
        img_filepath = url_for('static', filename = 'data/example/' + video_name + '.jpg')
        content.append([video_name, video_url, img_filepath])
    #print(content)
    return render_template('history.html', content = content)

@app.route('/WordCloudType')
def WordCloudType():
    return render_template('WordCloudType.html')

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5050)
    sys.exit()