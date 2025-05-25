import os
from dotenv import load_dotenv
import pathlib
from google.genai import types
from google import genai
import httpx
load_dotenv()

"""
# 讀取 .env 檔案
load_dotenv()

# 使用 os.getenv() 取得環境變數
key = os.getenv("GEMINI_API_KEY")
#print("我的金鑰是：", key)

client = genai.Client(api_key=key)
"""


def send_to_gemini(pdf:str, metadata:str, response_file_path:str):
  """使用 gemini 完成 ppt 結構

  Args:
      pdf (str): 論文 pdf path
      metadata (str): metadata path
      response_file_path: str
  """
  API_KEY = os.getenv('GEMINI_API_KEY')
  client = genai.Client(api_key=API_KEY)
  
  pdf_path = pathlib.Path(pdf)
  txt_path = pathlib.Path(metadata)
  with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()
  
  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        prompt, 
        types.Part.from_bytes(
          data=pdf_path.read_bytes(),
          mime_type='application/pdf',
        ),
        types.Part.from_bytes(
          data=txt_path.read_bytes(),
          mime_type='text/plain',
        ),
      ],
    config={
          "response_mime_type": "application/json",
      }
    )

  print(response.text)

  with open(response_file_path, "w", encoding="utf-8") as f:
    f.write(response.text)


if __name__ == '__main__':
  pdf_path = '2405.10530v1.pdf'
  metadata_path = 'output_metadata.txt'
  out_path = 'generate_output.txt'
  send_to_gemini(pdf_path, metadata_path, out_path)
