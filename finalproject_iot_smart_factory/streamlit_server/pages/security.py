
import streamlit as st
from PIL import Image
import time,datetime
import firebase_admin
from firebase_admin import credentials, db, storage

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate(r"C:\Users\user\finalproject\streamlit_server\test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://test-server-64fab-default-rtdb.firebaseio.com/'
    })
    
bucket = storage.bucket("test-server-64fab.appspot.com")
dir = db.reference()
time.sleep(1.0)

cho=["조현수","영업부","인턴"]
cha=["차은우","기획부","대리"]
ka=["카리나","총무부","과장"]
ea=["김영환","관리부","사원"]
kb=["강보경","기획부","사원"]


with st.empty():
    while True:
        col,_= st.columns([90,10])

        #col1.subheader("streaming")
        col.markdown(#카메라 스트리밍 주소
                f'<iframe src="http://10.10.13.47:3000/" width="800" height="600" style="border:none;"></iframe>',
                unsafe_allow_html=True,
            )
        name=''
        department=''
        position=''    
        current_time=''
        col.subheader("Infomation")
        face_dic = db.reference('face').get()

        if face_dic["flag"] == 1:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name=cho[0]
            department=cho[1]
            position=cho[2]
        elif face_dic["flag"] == 2:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name=cha[0]
            department=cha[1]
            position=cha[2]
        elif face_dic["flag"] == 3:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name=ka[0]
            department=ka[1]
            position=ka[2]
        elif face_dic["flag"] == 4:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name=ea[0]
            department=ea[1]
            position=ea[2]
        elif face_dic["flag"] == 5:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name=kb[0]
            department=kb[1]
            position=kb[2]
        elif face_dic["flag"] == 6:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
            name="!!미확인 출입자!!"
        elif face_dic["flag"] == 0:
            continue
        col.write(" ")
        col.write("성명:"+name)
        col.write("부서:"+department)
        col.write("직급:"+position)
        col.write("출입시간:"+current_time)
        dir.update({'face/flag':0})
        time.sleep(1.0)
