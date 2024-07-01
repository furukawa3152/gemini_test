import os

import google.generativeai as genai


# API-KEYの設定
GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

gemini_pro = genai.GenerativeModel("gemini-pro")
prompt = "こんにちは"
response = gemini_pro.generate_content(prompt)
print(response.text)