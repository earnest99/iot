import face_recognition
import cv2 , datetime, os,firebase_admin, time, threading
from flask import Flask, render_template, Response
import numpy as np
from firebase_admin import credentials,db
from firebase_admin import storage

global frame
video_capture = cv2.VideoCapture(0)
#Firebase database 인증 및 앱 초기화

cred = credentials.Certificate(r'C:\python_code_1/test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-server-64fab-default-rtdb.firebaseio.com/'
})
dir = db.reference('')


app = Flask(__name__)
# Storage 버킷 생성
bucket = storage.bucket("test-server-64fab.appspot.com")

# Load a sample picture and learn how to recognize it.
cho_image = face_recognition.load_image_file("cho.jpg")
cho_face_encoding = face_recognition.face_encodings(cho_image)[0]

# Load a second sample picture and learn how to recognize it.
cha_image = face_recognition.load_image_file("cha.jpg")
cha_face_encoding = face_recognition.face_encodings(cha_image)[0]

karina_image = face_recognition.load_image_file("karina.jpg")
karina_face_encoding = face_recognition.face_encodings(karina_image)[0]

earnest_image = face_recognition.load_image_file("earnest.jpg")
earnest_face_encoding = face_recognition.face_encodings(earnest_image)[0]

kang_image = face_recognition.load_image_file("kang.jpg")
kang_face_encoding = face_recognition.face_encodings(kang_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    cho_face_encoding,
    cha_face_encoding,
    karina_face_encoding,
    earnest_face_encoding,
    kang_face_encoding
]
known_face_names = [
    "cho",
    "cha",
    "karina",
    "earnest",
    "kang"
]
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
image_cnt =0

def generate_frames():
    global process_this_frame
    global frame
    global face_locations
    global face_names
    try : 
        while True:
            ret, frame = video_capture.read()
            # 카메라에서 프레임 읽기
            
            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                new_width = int(frame.shape[1] * 0.25)
                new_height = int(frame.shape[0] * 0.25)
                small_frame = cv2.resize(frame, (new_width, new_height))


                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                #rgb_small_frame = small_frame[:, :, ::-1]
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                try:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                
                # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    

                    if name in known_face_names :
                        member = True
                        image_save_on_off(member,name)
                    elif not name in known_face_names:
                        member = False
                        image_save_on_off(member,name)
                    else : pass
                except:
                    pass

            if not ret:
                break
            else:
                try:
                    # 프레임을 바이트로 변환하여 스트리밍
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if isinstance(frame, np.ndarray):
                        print("frame is a numpy ndarray")
                        frame = buffer.tobytes()
                        try:
                            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        except:
                            pass
                    else:
                        print("pass")
                except:
                    pass
        

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        pass


# Initialize some variables

def image_save_on_off(member,name):
    global image_cnt
    global frame
    if name == "cho":
        dir.update({'face/flag': 1})
    elif name == "cha":
        dir.update({'face/flag': 2})
    elif name == "karina":
        dir.update({'face/flag': 3})
    elif name == "earnest":
        dir.update({'face/flag': 4})
    elif name == "kang":
        dir.update({'face/flag': 5})
    else :
        dir.update({'face/flag': 6})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    t = threading.Thread(target=image_save_on_off)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
