from flask import Flask, render_template, Response, request, g, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__, template_folder='./templates', static_folder='./templates/static')

ALLOWED_EXTENSIONS = {'mp4'} #파일 업로드가 가능한 확장자 목록

@app.route('/')
def hello_world():
    return "Server is running!"

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/files', methods=['POST'])
def file_upload():
    os.makedirs('./templates/static/video', exist_ok=True) #디렉토리가 없을 경우 생성

    f = request.files['file']

    if f and allowed_file(f.filename):
        f.save('./templates/static/video/' + secure_filename(f.filename))
        return render_template("success.html")
    else:
        return render_template("wrong.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/files', methods=['GET'])
def get_video_list():
    path = './templates/static/video'
    file_list = os.listdir(path)
    return jsonify(file_list)

@app.route('/files/<string:file>', methods=['GET'])
def get_video(file):
    return send_file("./templates/static/video/"+file)

@app.route('/video_feed')
def video_feed():
    return Response(get_video(), content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/check')
def check():
    def generate():        
        while True:
            yield g.isBlackIce
    return Response(generate(), content_type="text/plain")

def get_video():
    cap = cv2.VideoCapture(0)

    while True:
        ret, image = cap.read()

        if not ret:
            break

        processed_frame = process_frame(image) #블랙아이스 판단

        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def process_frame(frame):

    # isBlackIce = False
    
    #Processing: 블랙 아이스 유무에 따라 isBlackIce 변수 조정
    
    # g.isBlackIce = isBlackIce

    return frame

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')