import streamlit as st
from st_files_connection import FilesConnection
import json


conn = st.experimental_connection('gcs', type=FilesConnection)
file_path = "food-bro/instruct.json"


# Read the file as ordinary text file
with conn.open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    st.write(data)

data['Martin'] = {'polozka' : 'nehodnota'}


with conn.open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
