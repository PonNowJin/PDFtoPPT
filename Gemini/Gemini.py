import os
from dotenv import load_dotenv
import pathlib
from google.genai import types
from google import genai

# 讀取 .env 檔案
load_dotenv()

# 使用 os.getenv() 取得環境變數
key = os.getenv("GEMINI_API_KEY")
#print("我的金鑰是：", key)

client = genai.Client(api_key=key)

pdf_path = pathlib.Path('2405.10530v1.pdf')
txt_path = pathlib.Path('output_metadata.txt')
with open("prompt.txt", "r", encoding="utf-8") as f:
  prompt = f.read()
#prompt = "pdf檔案為一篇論文，txt檔的內容為此論文pdf中的圖片資訊，'page'為圖片在論文中的頁數，'bbox'為圖片在該頁的位置，'caption'為圖片敘述，'image_name'為圖片存在本機的檔名，請在理解論文後，幫我用python-pptx製作一份ppt"

response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents=[
      types.Part.from_bytes(
        data=pdf_path.read_bytes(),
        mime_type='application/pdf',
      ),
      types.Part.from_bytes(
        data=txt_path.read_bytes(),
        mime_type='text/plain',
      ),
      prompt
  ])

print(response.text)
with open("generate_output.txt", "w", encoding="utf-8") as f:
  f.write(response.text)