import streamlit as st
from PIL import Image
import time
import firebase_admin
from firebase_admin import credentials, db, storage
from streamlit_option_menu import option_menu


#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate(r"C:\Users\user\finalproject\streamlit_server\test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://test-server-64fab-default-rtdb.firebaseio.com/'
    })

box_none = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\box_none.png')
box_in = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\box_in.png')
box_mid = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\box_mid.png')
box_out = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\box_out.png')
lamp_none = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\lamp_none.png')
lamp_red = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\lamp_red.png')
lamp_green = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\lamp_green.png')
lamp_yellow = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\lamp_yellow.png')

def print_factory_value(factory1_dic,factory2_dic):
    print("="*50)
    print("컨베이어1 상태")
    print("컨베이어속도:", factory1_dic["convayor_speed"])
    print("램프상태:", factory1_dic["lamp"])
    print("입구 근접센서 상태:", factory1_dic["sensor_in"])
    print("중간 근접센서 상태:", factory1_dic["sensor_mid"])
    print("출구 근접센서 상태:", factory1_dic["sensor_out"])

    print("="*50)

    print("컨베이어2 상태")
    print("컨베이어속도:", factory2_dic["convayor_speed"])
    print("램프상태:", factory2_dic["lamp"])
    print("입구 근접센서 상태:", factory2_dic["sensor_in"])
    print("중간 근접센서 상태:", factory2_dic["sensor_mid"])
    print("출구 근접센서 상태:", factory2_dic["sensor_out"])
    print("="*50)


dir = db.reference()
# Storage 버킷 생성
bucket = storage.bucket("test-server-64fab.appspot.com")

time.sleep(1.0)
factory1_image = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\factory1.jpg')
factory2_image = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\factory2.jpg')

cola,_,colm,_=st.columns([20,15,50,15])
image = Image.open(r"C:\Users\user\finalproject\streamlit_server\images\iot.jpg")
cola.image(image, caption="", use_column_width=True)
colm.title("스마트 팩토리")

col0,_,colb,_ = st.columns([60,10,20,10])
col0.write(#카메라 스트리밍 주소
    f'<iframe src="http://10.10.13.47:5000/" width="800" height="600"></iframe>',
    unsafe_allow_html=True,
)
if colb.button("긴급정지!"):
    dir.update({'server/emergency':1})
with st.empty():
    while True:
        factory1_dic = db.reference('factory1').get()
        factory2_dic = db.reference('factory2').get()
        #print_factory_value(factory1_dic,factory2_dic)

        
        
        col1, col2, col3= st.columns([4,4,4],gap="large")
        
        

        # 오른쪽 공정 이미지 출력
        col1.subheader("공정1")
        if factory1_dic["lamp"] == "RED":  col1.image(lamp_red,width=400)
        elif factory1_dic["lamp"] == "YELLOW":  col1.image(lamp_yellow,width=400)
        elif factory1_dic["lamp"] == "GREEN":  col1.image(lamp_green,width=400)
        else: col1.image(lamp_none,width=400)
        
        if factory1_dic["sensor_in"] == 1:  col1.image(box_out,width=500)
        elif factory1_dic["sensor_mid"] == 1:  col1.image(box_mid,width=500)
        elif factory1_dic["sensor_out"] == 1:  
            col1.image(box_in,width=500)
            image_name = factory1_dic["image_name"]
            blob = bucket.blob(f"factory1/{image_name}")
            download_path = r"C:\Users\user\finalproject\streamlit_server\images\factory1.jpg"
            blob.download_to_filename(download_path)
            factory1_image = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\factory1.jpg')
        else: col1.image(box_none,width=500)
        col1.subheader("벨트속도:" + str(factory1_dic["convayor_speed"]))

        
        col1.image(factory1_image,width=480)

        factory1_dic = db.reference('factory1').get()
        #print(factory2_image_name)
        factory1_image_name = factory1_dic["image_name"] if not isinstance(factory1_dic, str) else factory1_dic
        col1.write(factory1_image_name)

        # 왼쪽 공정 이미지 출력
        col3.subheader("공정2")
        if factory2_dic["lamp"] == "RED":  col3.image(lamp_red,width=400)
        elif factory2_dic["lamp"] == "YELLOW":  col3.image(lamp_yellow,width=400)
        elif factory2_dic["lamp"] == "GREEN":  col3.image(lamp_green,width=400)
        else: col3.image(lamp_none,width=400)
        
        if factory2_dic["sensor_in"] == 1:  col3.image(box_out,width=500)
        elif factory2_dic["sensor_mid"] == 1:  col3.image(box_mid,width=500)
        elif factory2_dic["sensor_out"] == 1:  
            col3.image(box_in,width=500)
            image_name = factory2_dic["image_name"]
            blob = bucket.blob(f"factory2/{image_name}")
            download_path = r"C:\Users\user\finalproject\streamlit_server\images\factory2.jpg"
            blob.download_to_filename(download_path)
            time.sleep(1.0)
            factory2_image = Image.open(r'C:\Users\user\finalproject\streamlit_server\images\factory2.jpg') 
        else: col3.image(box_none,width=500)
        col3.subheader("벨트속도:" + str(factory2_dic["convayor_speed"]))

        
        col3.image(factory2_image,width=480)

        factory2_dic = db.reference('factory2').get()
        #print(factory2_image_name)
        factory2_label = factory2_dic["label"] if not isinstance(factory2_dic, str) else factory2_dic
        col3.write("detected_"+factory2_label)
        

        
        
        time.sleep(0.2)
