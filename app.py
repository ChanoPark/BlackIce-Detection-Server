from flask import Flask, render_template, Response, g
import cv2
app = Flask(__name__, template_folder='./templates', static_folder='./templates/static')


@app.route('/')
def hello_world():
    return "Server is running!"

@app.route('/main')
def main():
    return render_template('index.html')

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