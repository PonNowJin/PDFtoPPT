import time
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))  # 加入當前目錄

from FetchImage.extracted_yolo import pdf_to_images, detect_and_annotate_images
from Gemini.Gemini import send_to_gemini
from pptx_api import json_to_pptx

PDF_IMG_DIR = 'temp_output/pdf_pages'  # temp資料夾 用於存轉檔後的pdf
OUTPUT_ANNOTATED_DIR = 'temp_output/annotated_results' # 用於存標註好的結果（要將debug開啟才有用）
METADATA_PATH = 'temp_output/output_metadata.json'
GEMINI_OUTPUT_PATH = 'temp_output/gemini_response.txt'
FINALL_PPT = 'output_pptx/final.pptx'
FINALL_PPT_WM = 'output_pptx/final_wm.pptx'
CROP_IMGS_DIR = 'Crop_imgs'


def paper_to_slide(pdf_path, output_pptx_path, theme_pptx_path):
    try:
        #論文圖片處理 metadata 生成
        print("將 PDF 頁面轉換為圖片...")
        image_paths = pdf_to_images(pdf_path, PDF_IMG_DIR)

        print("使用 YOLO 偵測圖區...")
        metadata = detect_and_annotate_images(image_paths, OUTPUT_ANNOTATED_DIR, crop_img_dir=CROP_IMGS_DIR,debug=False)

        # 存檔 metadata
        with open(METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print("圖片抓取完成")
        
        # Gemini 處理
        send_to_gemini(pdf_path, METADATA_PATH, GEMINI_OUTPUT_PATH)
        
        # 製作pptx
        json_to_pptx(GEMINI_OUTPUT_PATH, output_pptx_path, output_pptx_path, image_dir=CROP_IMGS_DIR, template=theme_pptx_path,premium=True)

        return True

    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        
        return False
