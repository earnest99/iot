import threading
import streamlit as st
import time
import queue


q = queue.Queue()

def test_run():
    for x in range(1, 100):
        val = x
        multiply = val * 10
        q.put((val, multiply))
        print(val)
        time.sleep(1)


def update_dashboard():
    while True:
        val, multiply = q.get()

        col1, col2 = st.columns(2)
        col1.metric(label="Current Value", value=val)
        col2.metric(label="Multiply by 10 ", value=multiply)


threading.Thread(target=test_run).start()

# dashboard title
st.title("Streamlit Learning")

with st.empty():
    update_dashboard()