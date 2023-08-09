import streamlit as st
import time
from PIL import Image
import random

image_holder = st.empty()

def update_dashboard():
    while True:
        box_in = Image.open(r'C:\python_project\streamlit_server\images\box_in.png')
        box_mid = Image.open(r'C:\python_project\streamlit_server\images\box_mid.png')
        box_out = Image.open(r'C:\python_project\streamlit_server\images\box_out.png')

        box_list = [box_in,box_mid,box_out]

        rand = int(random.randint(0,2))
        print("랜덤",rand)

        image_holder.image(box_list[rand],width=300)
        time.sleep(2.0)


update_dashboard()