import streamlit as st
import os
import json
import openai
import base64, requests


api_key = st.secrets["openai_key"]

def answer_pic(image, prompt):
# Path to your image
    

    # Getting the base64 string
    base64_image = base64.b64encode(image.getvalue()).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()



image = st.file_uploader("Upload file", type = ["png", "jpg", "jpeg"])
prompt = st.text_input("What's your question?", value = "What’s in this image? Segregate all provided infromation and answer in json format.")

if st.button("Ask"):
    if image:
        st.image(image)
        response = answer_pic(image, prompt)['choices'][0]['message']['content']
        st.write(response)
    else:
        st.write("Please upload an image")

