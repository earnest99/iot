import time
import serial
import serial.tools.list_ports
import threading,firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate(r'C:\Users\kangb\Desktop\streamlit_server\test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-server-64fab-default-rtdb.firebaseio.com/'
})
dir = db.reference()

def send_bright():
    sendData = f"BRIGHT=?\n"
    my_serial.write( sendData.encode() )
    

def send_temperature():
    sendData = f"TEMPERATURE=?\n"
    my_serial.write( sendData.encode() )
    

def send_humidity():
    sendData = f"HUMIDITY=?\n"
    my_serial.write( sendData.encode() )
    

serial_receive_data = ""
def serial_read_thread():
    global serial_receive_data
    
    while True:
        read_data = my_serial.readline()
        serial_receive_data = read_data.decode()
        

def send_vr_bright_1sec():
    t2 = threading.Timer(1, send_vr_bright_1sec)
    t2.daemon = True
    t2.start()
    send_temperature()
    time.sleep(0.3)
    send_humidity()
    time.sleep(0.3)
    send_bright()
    time.sleep(0.3)

def main():
    try:
        send_vr_bright_1sec()
        global serial_receive_data
        while True:
            if "TEMPERATURE=" in serial_receive_data:
                TEMPERATURE = float(serial_receive_data[12:])
                print("온도:",TEMPERATURE)
                dir.update({'environment/TEMPERATURE': f'{TEMPERATURE}'})
                serial_receive_data = ""
            if "HUMIDITY=" in serial_receive_data:
                HUMIDITY = float(serial_receive_data[9:])
                print("습도:",HUMIDITY)
                dir.update({'environment/HUMIDITY': f'{HUMIDITY}'})
                serial_receive_data = ""
            if "BRIGHT=" in serial_receive_data:
                BRIGHT = float(serial_receive_data[7:])
                print("조도:" ,BRIGHT)
                dir.update({'environment/BRIGHT': f'{BRIGHT/10}'}) #조도 변환 상수 0.1로 가정
                serial_receive_data = ""

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    
    my_serial = serial.Serial('COM5', baudrate=9600, timeout=1.0)
    print("COM5 포트에 아두이노가 연결되었습니다.")
    time.sleep(2.0)

    t1 = threading.Thread(target=serial_read_thread)
    t1.daemon = True
    t1.start()
    
    main()
    
    my_serial.close()