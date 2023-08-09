import streamlit as st
from PIL import Image
import time


col1, col2, col3= st.columns([4,2,4])


with col1:
    box_in = Image.open(r'C:\python_project\streamlit_server\images\box_in.png')
    box_mid = Image.open(r'C:\python_project\streamlit_server\images\box_mid.png')
    box_out = Image.open(r'C:\python_project\streamlit_server\images\box_out.png')

    box_list = [box_in,box_mid,box_out]

    st.session_state['image2'] = box_in
    st.image(st.session_state['image2'])

    for box in box_list:
        st.session_state['image2'] = box
        st.image(st.session_state['image2'])
        time.sleep(1.0)

with col3:
    box_image = Image.open(r'C:\python_project\streamlit_server\images\box.png')
    convayor_image = Image.open(r'C:\python_project\streamlit_server\images\convayor.png')
    st.image(box_image,width=80)
    st.image(convayor_image,width=400)



