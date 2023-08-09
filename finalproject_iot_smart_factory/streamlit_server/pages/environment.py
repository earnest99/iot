import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate(r"C:\Users\user\finalproject\streamlit_server\test-server-64fab-firebase-adminsdk-hfv3y-8c7be173e8.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://test-server-64fab-default-rtdb.firebaseio.com/'
    })

# Streamlit 앱 초기화
st.set_page_config(page_title="environment_page")

# 데이터를 저장할 빈 데이터 프레임 생성
cumulative_df = pd.DataFrame(columns=['timestamp'])

# 빈 차트를 생성하여 차트 업데이트에 사용
chart = st.empty()

def plot_environment_values(environment_dic):
    
    global cumulative_df,new_data  # 전역 변수로 설정
    
    # 새로운 데이터 프레임 생성
    new_data = pd.DataFrame(environment_dic, index=[0])
    new_data['timestamp'] = pd.to_datetime(datetime.now())
    
    # cumulative_df에 새로운 데이터 추가
    cumulative_df = pd.concat([cumulative_df, new_data], ignore_index=True)
    
    # 데이터를 시간순으로 정렬
    cumulative_df = cumulative_df.sort_values(by='timestamp')
    
    # 시각화
    fig = px.line(cumulative_df, x='timestamp', y=list(environment_dic.keys()), title='환경 모니터링')
    
    # 빈 차트 업데이트
    chart.plotly_chart(fig)
    

# Streamlit 앱 실행
with st.empty():
    while True:
        col,_= st.columns([90,10])
        nn={}
        environment_dic = db.reference('environment').get()
        if environment_dic:
            plot_environment_values(environment_dic)
            nn=new_data
        else:
            st.warning("환경 데이터를 찾을 수 없습니다.")

        col.write(nn)
        # 5초마다 업데이트되도록 변경
        time.sleep(5)
