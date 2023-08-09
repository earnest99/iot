import cv2, firebase_admin
from flask import Flask, render_template, Response
from firebase_admin import credentials,db

cred = credentials.Certificate(r'C:\Users\user\finalproject\streamlit_server\test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-server-64fab-default-rtdb.firebaseio.com/'
})
dir = db.reference('factory1')

app = Flask(__name__)
dir.update({'cam_address' : '10.10.13.179:5000'})

# 카메라 초기화
camera = cv2.VideoCapture(1)

def generate_frames():
    while True:
        # 카메라에서 프레임 읽기
        success, frame = camera.read()
        if not success:
            break
        else:
            # 프레임을 바이트로 변환하여 스트리밍
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)