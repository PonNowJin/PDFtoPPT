import fitz  # PyMuPDF
import cv2
import os
from ultralytics import YOLO
import numpy as np

CROP_IMAGE_DIR = "Crop_imgs"

# 載入你訓練好的模型
model = YOLO("FetchImage/yolo_model/best_2.pt")


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
        crop_and_save_image(img, boxes_record, CROP_IMAGE_DIR)

        annotated_path = os.path.join(output_folder, os.path.basename(img_path))
        cv2.imwrite(annotated_path, img)
        print(f"已標註：{annotated_path}")
        
        
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

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box['bbox']
        label = box.get('label', 'object')
        page_num = box['page']
        cropped_img = img[y1:y2, x1:x2]

        filename = f"{prefix}_{page_num}_{label}_{i+1}.png"
        path = os.path.join(output_dir, filename)
        cv2.imwrite(path, cropped_img)
        cropped_paths.append(path)

    print(f"已儲存 {len(cropped_paths)} 張切割圖到 {output_dir}")
    return cropped_paths




if __name__ == "__main__":
    pdf_path = "/Users/ponfu/Downloads/2101.01169v5.pdf"
    tmp_image_folder = "pdf_pages"
    output_annotated_folder = "annotated_results"

    print("將 PDF 頁面轉換為圖片...")
    image_paths = pdf_to_images(pdf_path, tmp_image_folder)

    print("使用 YOLO 偵測圖區...")
    detect_and_annotate_images(image_paths, output_annotated_folder)

    print("完成！所有結果儲存在:", output_annotated_folder)
