import streamlit as st
import concurrent.futures
import time
import os
from openai import OpenAI
import anthropic
import google.generativeai as genai


def gemini_call(input_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    start_time = time.time()  # 開始時間を記録
    gemini_pro = genai.GenerativeModel("gemini-1.5-pro")
    prompt = input_text
    response = gemini_pro.generate_content(prompt)
    end_time = time.time()  # 終了時間を記録
    elapsed_time = end_time - start_time  # 経過時間を計算
    return ["gemini1.5-pro", response.text, f"Time: {elapsed_time:.2f} seconds"]


def Claude_call(input_text):
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
    )
    start_time = time.time()  # 開始時間を記録
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": input_text}
        ]
    )
    end_time = time.time()  # 終了時間を記録
    elapsed_time = end_time - start_time  # 経過時間を計算
    return ["claude3.5sonnet", message.content[0].text, f"Time: {elapsed_time:.2f} seconds"]


def gpt_call(input_text):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    start_time = time.time()  # 開始時間を記録
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model="gpt-4o",
    )
    end_time = time.time()  # 終了時間を記録
    elapsed_time = end_time - start_time  # 経過時間を計算
    return ["GPT-4o", chat_completion.choices[0].message.content, f"Time: {elapsed_time:.2f} seconds"]


# 並列処理で関数を実行する
def run_functions_parallel(input_text):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(gemini_call, input_text),
            executor.submit(Claude_call, input_text),
            executor.submit(gpt_call, input_text)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                st.header(result[0])
                st.text(result[2])
                st.markdown(result[1])
            except Exception as e:
                st.text(f"Generated an exception: {e}")



# Streamlit UI
st.title("GPT4o vs claude3.5sonnet vs gemini-pro")
# サイドバーにフォームを作成K
with st.sidebar:
    GOOGLE_API_KEY = st.text_input("GOOGLE_API_KEY")
    ANTHROPIC_API_KEY = st.text_input("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = st.text_input("OPENAI_API_KEY")

input_text = st.text_area("質問を入れてください")
if st.button("回答する"):
    if input_text:
        st.header("回答の早い順に表示します。")
        run_functions_parallel(input_text)
    else:
        st.write("質問を入れてください")