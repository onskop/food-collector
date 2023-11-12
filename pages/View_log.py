import streamlit as st
import os, io
from st_files_connection import FilesConnection
import base64


conn = st.connection('gcs', type=FilesConnection)
textpath = 'food-bro/img_data.json'
imgpath = 'food-bro/img-captures'

def load_img(path, filename):
    with conn.open(path + '/' + filename, 'rb') as f:
        image = io.BytesIO(f.read())
    return image

def load_log(path):
    with conn.open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data



if st.button('Load'):
    data = load_log(textpath)
    datalist = data.split('PIC: ')
    for i in range(1,len(datalist)):
        st.image(load_img(imgpath, datalist[i].split('\n')[0]))
        st.write(datalist[i])
        st.write('---')
