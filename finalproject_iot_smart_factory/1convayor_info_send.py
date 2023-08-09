import cv2, time,serial.tools.list_ports,threading,datetime, os,firebase_admin,torch
from firebase_admin import credentials,db
from firebase_admin import storage
from numpy import random
import torch

# 웹캠 열기
cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate(r'C:\python_code_1/test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-server-64fab-default-rtdb.firebaseio.com/'
})
dir = db.reference('factory1')



# Storage 버킷 생성
bucket = storage.bucket("test-server-64fab.appspot.com")

# Arduino Uno를 찾아서 시리얼 포트에 연결합니다.
def connect_to_arduino_uno():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino Uno" in port.description:
            try:
                ser = serial.Serial(port.device, baudrate=9600)
                return ser
            except serial.SerialException:
                pass
    return None

serial_receive_data = ""
# 시리얼통신 수신 쓰레드 함수
def serial_read_thread():
    global serial_receive_data
    while True:
        read_data = ser.readline().decode()
        serial_receive_data = read_data

#컨베이어벨트 제어
def send_conveyor_speed(speed):
    if 0 <= speed <=255:
        ser.write(f"CV_MOTOR={speed}\n".encode())
        dir.update({'convayor_speed': speed})
    else:
        print("0~255사이의 값을 입력하세요")

def upload_image_to_storage(image_path, ft):
    # Storage에 이미지 파일 업로드
    current_time = datetime.datetime.now().strftime(f"%Y%m%d%H%M%S")
    jpg = f"{current_time}_{ft}.jpg"
    blob = bucket.blob(f"factory1/{jpg}")
    blob.upload_from_filename(image_path)
    dir.update({'image_name': f'{jpg}'})
    ft=""
    
    print('이미지가 성공적으로 업로드되었습니다.')


# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

# 쓰레드를 시작합니다.
t1 = threading.Thread(target=serial_read_thread)
t1.daemon = True
t1.start()
image_cnt = 0

# YOLOv5 모델 정의
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

if torch.cuda.is_available():
    model = model.cuda()

def send_lamp_red(on_off):
    if on_off:
        ser.write("LAMP_RED=ON\n".encode())
    else:
        ser.write("LAMP_RED=OFF\n".encode())

def send_lamp_yellow(on_off):
    if on_off:
        ser.write("LAMP_YELLOW=ON\n".encode())
    else:
        ser.write("LAMP_YELLOW=OFF\n".encode())

def send_lamp_green(on_off):
    if on_off:
        ser.write("LAMP_GREEN=ON\n".encode())
    else:
        ser.write("LAMP_GREEN=OFF\n".encode())


def send_servo_1_angle(angle=80):
    if 60 <= angle <= 130:
        ser.write(f"SERVO_1={angle}\n".encode())
    else:
        print("60~130사이의 값을 입력하세요")

def send_servo_2_angle(angle=180):
    if 0 <= angle <= 180:
        ser.write(f"SERVO_2={angle}\n".encode())
    else:
        print("0~180사이의 값을 입력하세요")

def send_servo_3_angle(angle=100):
    if 30 <= angle <= 120:
        ser.write(f"SERVO_3={angle}\n".encode())
    else:
        print("30~120사이의 값을 입력하세요")

def send_catch_on_off(on_off):
    if on_off:
        ser.write("CATCH=ON\n".encode())
    else:
        ser.write("CATCH=OFF\n".encode())
def stop():
    ser.write("LAMP_RED=ON\n".encode())
    ser.write("LAMP_YELLOW=OFF\n".encode())
    ser.write("LAMP_GREEN=OFF\n".encode())
    dir.update({'lamp':"RED"})
    send_conveyor_speed(0)
    send_servo_1_angle(80)
    send_servo_2_angle(180)
    send_servo_3_angle(100)
    send_catch_on_off(False)
    dir.update({'server/emergency':0})

    
send_servo_1_angle(80)
send_servo_2_angle(180)
send_servo_3_angle(100)
send_catch_on_off(False)
label1 = ""

time.sleep(2.0)
try:
    print("start")
    dir.update({'sensor_in':0,
                'sensor_mid':0,
                'sensor_out':0,
                'lamp': 'OFF',})
    serial_receive_data = ""
    image_save_on_off = False
    while True:
    # 투입쪽에 물건이 들어오면 컨베이어 동작
        eg= db.reference('server').get()
        if eg['emergency']==1:
            stop()
        elif "PS_3=ON" in serial_receive_data:
            send_conveyor_speed(255)
            print(serial_receive_data)
            send_lamp_red(False)
            send_lamp_yellow(False)
            send_lamp_green(True)
            dir.update({'sensor_in':1,
                        'lamp': 'GREEN'})
        elif "PS_3=OFF" in serial_receive_data:
            dir.update({'sensor_in': 0})
        # 중앙센서 검출
        elif "PS_2=ON" in serial_receive_data:
            print(serial_receive_data)
            serial_receive_data = ""
            dir.update({'sensor_mid': 1})
            time.sleep(0.5)
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            folder_path = current_time
            os.makedirs(folder_path, exist_ok=True)
            image_save_on_off = True    
        elif "PS_2=OFF" in serial_receive_data:
            print(serial_receive_data)
            dir.update({'sensor_mid': 0})
            serial_receive_data = ""
            image_save_on_off = False
        elif "PS_1=ON" in serial_receive_data:
            if not label1 == "":
                serial_receive_data = ""
                dir.update({'sensor_out': 1})
                time.sleep(0.7)
                send_conveyor_speed(0)
                print("1.물건 잡음")
                send_servo_1_angle(130)
                send_servo_2_angle(176)
                send_servo_3_angle(100)
                time.sleep(1.0)
                send_catch_on_off(True)
                time.sleep(2.0)

                print("2.물건 올림")
                send_servo_1_angle(80)
                send_servo_2_angle(180)
                send_servo_3_angle(100)
                time.sleep(2.0)

                print("3.물건 이동")
                send_servo_1_angle(100)
                send_servo_2_angle(80)
                send_servo_3_angle(100)
                time.sleep(2.0)

                print("4.물건 내림")
                send_servo_1_angle(115)#높이
                send_servo_2_angle(85)#회전
                send_servo_3_angle(100)#길이
                time.sleep(2.0)
                send_catch_on_off(False)
                time.sleep(2.0)

                print("5.원위치")
                send_servo_1_angle(80)
                send_servo_2_angle(180)
                send_servo_3_angle(100)
                time.sleep(2.0)
                label1 =""
                dir.update({'sensor_out': 0})
                # 출구에서 물건이 나가면 컨베이어 멈춤
            else :
                dir.update({'sensor_out': 1})
        elif "PS_1=OFF" in serial_receive_data:
            send_lamp_yellow(True)
            send_lamp_green(False)
            send_lamp_red(False)
            print(serial_receive_data)
            serial_receive_data = ""
            dir.update({'sensor_out': 0,
                        'lamp': 'YELLOW'})
            time.sleep(2.0)
            send_conveyor_speed(0)
            label1 =""
            
        # 프레임 읽기
        ret, frame = cap.read()
        if ret:
            # 프레임 크기 조정
            frame = cv2.resize(frame, (640, 480))

            # 이미지를 모델에 입력
            results = model(frame)

            # 객체 감지 결과 얻기
            detections = results.pandas().xyxy[0]

            if not detections.empty:
                # 결과를 반복하며 객체 표시
                for _, detection in detections.iterrows():
                    x1, y1, x2, y2 = detection[['xmin', 'ymin', 'xmax', 'ymax']].astype(int).values
                    label = detection['name']
                    label1 = label
                    conf = detection['confidence']

                    # 박스와 라벨 표시
                    color = [int(c) for c in random.choice(range(256), size=3)]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,2)
            
        cv2.imshow("image", frame)
        


        #이미지를 저장
        if label1 == "" and image_save_on_off:
            image_path = f"{folder_path}/CV1_{image_cnt}_F.jpg"
            image_cnt += 1
            ft = "F"
            cv2.imwrite(image_path, frame)
            upload_image_to_storage(image_path, ft)
        elif not label1 == "" and image_save_on_off:
            image_path = f"{folder_path}/CV1_{image_cnt}_T.jpg"
            image_cnt += 1
            ft = "T"
            label1 =""
            cv2.imwrite(image_path, frame)
            upload_image_to_storage(image_path,ft)
        else : pass
            
            

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            send_conveyor_speed(0)
            send_lamp_red(True)
            send_lamp_yellow(False)
            send_lamp_green(False)
            break
except:
    print("error")
    send_conveyor_speed(0)
    send_servo_1_angle(80)
    send_servo_2_angle(180)
    send_servo_3_angle(100)
    send_catch_on_off(False)
    send_lamp_red(True)
    send_lamp_yellow(False)
    send_lamp_green(False)
    
    ser.close()
    cap.release()
    cv2.destroyAllWindows()



