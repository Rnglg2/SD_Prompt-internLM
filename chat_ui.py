import streamlit as st
from openai import OpenAI
import os
import json
import time
import requests
import base64
import hashlib

def image_ui():
    state = st.session_state
    st.sidebar.title("生成的图片")

    with st.sidebar.expander("查看生成的图片", expanded=False):
        if 'generated_images' in state:
            if state.generated_images:
                latest_image = state.generated_images[-1]
                image_path = f"{latest_image}.png"
                if os.path.exists(image_path):
                    with st.container():
                        st.image(image_path, caption=latest_image, use_column_width=True)
                        st.download_button(
                            label="下载图片",
                            data=open(image_path, "rb").read(),
                            file_name=f"{latest_image}.png",
                            mime="image/png",
                        )
                else:
                    st.warning(f"未找到图片文件: {image_path}")
            else:
                st.info("尚未生成任何图片。")
        else:
            st.info("尚未生成任何图片。")
def sendapi(prompt):
    url = sd_webui_api
    payload = {
        "prompt": prompt,
        "negative_prompt": "none",
        "styles": ["string"],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "string",
        "scheduler": "string",
        "batch_size": 1,
        "steps": int(step),
        "cfg_scale": float(cfg),
        "distilled_cfg_scale": 3.5,
        "width": int(image_w),
        "height": int(image_h),
    }

    try:
        response = requests.post(url=url, json=payload)
        response.raise_for_status()  
        r = response.json()
        if 'images' in r and r['images']:
            image_data = r['images'][0]
            filename = hashlib.md5(image_data.encode()).hexdigest() 
            with open(f"{filename}.png", 'wb') as f:
                f.write(base64.b64decode(image_data))
            if 'generated_images' not in st.session_state:
                st.session_state.generated_images = []
            st.session_state.generated_images.append(filename)
    except Exception as e:
        print(f"API发送失败: {e}")
        return filename 
    
def col():
    col1, col2 = st.columns([3, 2])
    #with col1
    with col2:
        state = st.session_state
        with st.expander("interlnLM设置", expanded=False):
            max_tokens = st.number_input("最大token长度", min_value=0, max_value=2048, value=100, step=1)
            temperature = st.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
            api_key = st.text_input("API Key", value="internlm2")
            base_url = st.text_input("Base URL", value="http://127.0.0.1:23333/v1")
            system_prompt = st.text_area("系统提示", value="你是一个SD提示词助手，你需要将用户的需求转换为stable diffusion的提示词，以tag的形式。并且服从用户的命令，完成用户的任务。")

            submit = st.button("保存interlnLM设置")
            if submit:
                state.max_tokens = max_tokens if max_tokens != 0 else state.max_tokens
                state.temperature = temperature
                state.api_key = api_key
                state.base_url = base_url
                state.message_history = []
                if system_prompt:
                    state.system_prompt = system_prompt
                    state.message_history.append({"role": "system", "content": system_prompt})
                state.client = OpenAI(api_key=state.api_key, base_url=state.base_url)

def chat_ui():
    state = st.session_state
    st.title("SD提示词助手")
    st.caption("Ver0.1")
    if 'button_clicked' not in state:
        state.button_clicked = False

    if "client" not in state:
        st.info("请配置的基本设置，其中API Key和Base URL是必须的。")
    else:
        user_input = st.chat_input("输入消息")
        if user_input:
            state.message_history.append({"role": "user", "content": user_input})
            if "max_tokens" in state:
                response = state.client.chat.completions.create(
                    model=state.client.models.list().data[0].id,
                    messages=state.message_history,
                    max_tokens=state.max_tokens,
                    temperature=state.temperature
                )
            else:
                response = state.client.chat.completions.create(
                    model=state.client.models.list().data[0].id,
                    messages=state.message_history,
                    temperature=state.temperature
                )
            assistant_message = response.choices[0].message.content
            state.message_history.append({"role": "assistant", "content": assistant_message})

            st.chat_message("assistant").write(assistant_message)

            if st.button("发送到生图api", on_click=lambda: sendapi(assistant_message)):
                pass
        for message in state.message_history:
            if message["role"] == "system":
                continue
            else:
                st.chat_message(message["role"]).write(message["content"])
def side_bar():
    global image_h,image_w,step,cfg,sd_webui_api
    st.sidebar.title("Stable diffusion设置")
    state = st.session_state
    with st.sidebar.form(key="settings"):
        sd_webui_api= st.text_input("sd-api-url",value="http://127.0.0.1:7860/sdapi/v1/txt2img")
        image_h = st.number_input("图片高度", min_value=64, max_value=2048, value=896, step=32)
        image_w = st.number_input("图片宽度", min_value=64, max_value=2048, value=1152, step=32)
        step=st.number_input("Step", min_value=1, max_value=150, value=25, step=1)
        cfg=st.number_input("CFG", min_value=1.0, max_value=30.0, value=5.5, step=0.5)
        #after_Detailer=st.checkbox("after_Detailer",value=False)
        submit = st.form_submit_button("保存SD设置")
        if submit:
            state.image_h=image_h
            state.image_w=image_w
            state.sd_webui_api=sd_webui_api
            state.step=step
            state.cfg=cfg
            #state.after_Detailer=after_Detailer
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(state.message_history, f, ensure_ascii=False)
            pass
        state.message_history = []
        st.rerun()
    pass

if __name__ == "__main__":
    col()
    side_bar()
    chat_ui()
    image_ui()
    pass

    
