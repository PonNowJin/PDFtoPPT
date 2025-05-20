import fitz  # PyMuPDF
import cv2
import os
import re
import json
import pytesseract
from ultralytics import YOLO
import numpy as np

CROP_IMAGE_DIR = "Crop_imgs_demo"

# 載入你訓練好的模型
model = YOLO("FetchImage/yolo_model/best_3.pt")


# pdf -> png
def pdf_to_images(pdf_path, output_folder, dpi=300):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)
        output_path = os.path.join(output_folder, f"page_{page_num+1}.png")
        pix.save(output_path)
        image_paths.append(output_path)

    return image_paths


# YOLO 推論
def detect_and_annotate_images(image_paths, output_folder, debug=False):
    os.makedirs(output_folder, exist_ok=True)
    metadata = []

    for img_idx, img_path in enumerate(image_paths):
        results = model(img_path)
        img = cv2.imread(img_path)
        boxes_record = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                boxes_record.append({'bbox': [x1, y1, x2, y2], 'page': img_idx, 'label': label})
                
                # 標記在原圖上
                if (debug):
                    # 粗紅色框（加大線寬）
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=4)

                    # 粗紅字（黑底提高可視性）
                    text = f'{label} {conf:.2f}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.8
                    thickness = 3
                    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                    text_w, text_h = text_size

                    # 黑底方塊先畫在文字底下
                    cv2.rectangle(img, (x1, y1 - text_h - 8), (x1 + text_w + 4, y1), (0, 0, 0), -1)
                    # 再畫紅色文字
                    cv2.putText(img, text, (x1 + 2, y1 - 4), font, font_scale, (0, 0, 255), thickness)
                
        # 裁減
        temp_metadata = crop_and_save_image(img, boxes_record, CROP_IMAGE_DIR)
        metadata += temp_metadata
        
        if (debug):
            annotated_path = os.path.join(output_folder, os.path.basename(img_path))
            cv2.imwrite(annotated_path, img)
            print(f"已標註：{annotated_path}")
            
    return metadata
        
        
# 裁減
def crop_and_save_image(img, boxes, output_dir, prefix="crop", label_map=None):
    """
    從原圖中裁切出每個 box 區域並存檔

    Args:
        img: 原始影像 (BGR 格式)
        boxes: list of dict, 每個 dict 格式為 {'bbox': [x1, y1, x2, y2], 'label': str}
        output_dir: 儲存目錄
        prefix: 檔名前綴
        label_map: 類別名稱對應顏色（可選）

    Returns:
        cropped_paths: list of 儲存後圖片路徑
    """
    os.makedirs(output_dir, exist_ok=True)
    cropped_paths = []
    metadata = []

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box['bbox']
        label = box.get('label', 'object')
        page_num = box['page']
        cropped_img = img[y1:y2, x1:x2]

        filename = f"{prefix}_{page_num+1}_{label}_{i+1}.png"
        path = os.path.join(output_dir, filename)
        cv2.imwrite(path, cropped_img)
        cropped_paths.append(path)
        
        # 抓 caption
        caption = extract_caption_near_image(img, x1, y1, x2, y2)
        
        # 加入metadata
        metadata.append([{"page": page_num,
                        "bbox": [x1, y1, x2, y2],
                        "caption": caption,
                        "image_name": filename
                        }])

    print(f"已儲存 {len(cropped_paths)} 張切割圖到 {output_dir}")
    return metadata


# 模糊 keyword 比對 (OCR容錯)
def is_caption_keyword(line):
    line_lower = line.lower()
    # 定義模糊 pattern
    patterns = [
        r'f[\W_]*[i1l|I][\W_]*[gq9]',                 # fig, flg, f1g
        r'f[\W_]*[i1l|I][\W_]*[gq9][\W_]*[uüv][\W_]*[r][\W_]*[e3]',  # figure
        r't[\W_]*[a@][\W_]*[b6][\W_]*[l1i|I][\W_]*[e3]',  # table
        r'圖[\d一二三四五六七八九十]',              # 中文圖
        r'圖表[\d一二三四五六七八九十]',
    ]
    return any(re.search(p, line_lower) for p in patterns)



# 抓取圖片描述
def extract_caption_near_image(img, x1, y1, x2, y2, padding=100, max_lines=8):
    """_summary_

    Args:
        img : 原始影像 (RGB格式)
        x1, x2, y1, y2: 四點座標
        padding (int, optional): 尋找目標圖上下區域, Defaults to 100.
        max_lines (int, optional): caption 最大行數, Defaults to 8.

    Returns:
        string: caption
    """
    h, w = img.shape[:2]
    
    # 限制邊界（圖片上下尋找）
    y_start = max(0, y1-padding)
    y_end = min(h, y2+padding)
    roi = img[y_start:y_end, x1:x2]
    
    # 轉灰階 + OCR
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang="eng+chi_tra")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    capturing = False
    caption_count = 0
    caption_lines = []

    # 判斷是否包含特定文字(若有：擷取到空行處)
    for i, line in enumerate(lines):
        lower = line.lower()
        if is_caption_keyword(line):
            capturing = True
            caption_lines.append(line.strip())
            caption_count+=1
            
        elif capturing:
            if line.strip() == "":
                break
            caption_lines.append(line.strip())
            caption_count+=1
            
        if caption_count >= max_lines:
            break
            
    return ' '.join(caption_lines)



if __name__ == "__main__":
    pdf_path = "2405.10530v1.pdf"
    tmp_image_folder = "pdf_pages"
    output_annotated_folder = "annotated_results"

    print("將 PDF 頁面轉換為圖片...")
    image_paths = pdf_to_images(pdf_path, tmp_image_folder)

    print("使用 YOLO 偵測圖區...")
    metadata = detect_and_annotate_images(image_paths, output_annotated_folder)
    
    # 存檔 metadata
    with open('output_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print("完成！所有結果儲存在:", output_annotated_folder)
