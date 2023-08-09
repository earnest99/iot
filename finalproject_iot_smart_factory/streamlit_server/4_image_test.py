import streamlit as st
from PIL import Image
import time
import random

box_in = Image.open(r'C:\python_project\streamlit_server\images\box_in.png')
box_mid = Image.open(r'C:\python_project\streamlit_server\images\box_mid.png')
box_out = Image.open(r'C:\python_project\streamlit_server\images\box_out.png')
box_list = [box_in,box_mid,box_out]

lamp_none = Image.open(r'C:\python_project\streamlit_server\images\lamp_none.png')
lamp_red = Image.open(r'C:\python_project\streamlit_server\images\lamp_red.png')
lamp_green = Image.open(r'C:\python_project\streamlit_server\images\lamp_green.png')
lamp_yellow = Image.open(r'C:\python_project\streamlit_server\images\lamp_yellow.png')
lmap_list = [lamp_red,lamp_green,lamp_yellow]

left_convayor = st.empty()
right_convayor = st.empty()

with st.empty():
    while True:
        col1, col2, col3= st.columns([4,3,4],gap="large")
        rand = int(random.randint(0,2))
        print("랜덤",rand)
        col1.image(lmap_list[rand],width=400)
        col1.image(box_list[rand],width=500,caption="공정2")

        rand = int(random.randint(0,2))
        print("랜덤",rand)
        col3.image(lmap_list[rand],width=400)
        col3.image(box_list[rand],width=500,caption="공정1")
        
        time.sleep(2.0)



