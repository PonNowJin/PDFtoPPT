from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.dml.color import RGBColor
import json
import os
from PIL import Image
import random

def json_to_pptx(json_data, output_path="output.pptx", output_watermark_path="output_watermark.pptx",image_dir=None, prime=False):
    # jsonlike_txt to json
    with open(json_data, "r", encoding="utf-8") as f:
        try:
            content = f.read().strip()
            if not content:
                raise ValueError("檔案為空，無法解析")
            data = json.loads(content)
            # print(data)
        except json.JSONDecodeError as e:
            print("JSON 解析錯誤：", e)
        except Exception as e:
            print("其他錯誤：", e)

    # init ppt
    prs = Presentation()

    for idx, slide_data in enumerate(data):
        # print(slide_data, flush=True)
        # 封面頁
        if idx == 0:
            # 新增一頁標題投影片
            slide = prs.slides.add_slide(prs.slide_layouts[0])

            # 設定標題與副標題文字
            title = slide.shapes.title
            subtitle = slide.placeholders[1]
            title.text = slide_data["title"]
            subtitle.text = slide_data["subtitle"]
            continue
            
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # 空白版面

        # 加入標題
        if "title" in slide_data:
            title_shape = slide.shapes.title
            if not title_shape:
                title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
            title_tf = title_shape.text_frame
            title_tf.text = slide_data["title"]
            title_tf.paragraphs[0].font.size = Pt(32)
            title_tf.paragraphs[0].font.bold = True

        # 加入內文（子彈點）
        if "body" in slide_data:
            left = Inches(1)
            top = Inches(1.5)
            width = Inches(8)
            height = Inches(5)

            textbox = slide.shapes.add_textbox(left, top, width, height)
            tf = textbox.text_frame
            tf.word_wrap = True

            for idx, bullet in enumerate(slide_data["body"]):
                p = tf.add_paragraph() if idx != 0 else tf.paragraphs[0]
                p.text = bullet
                p.level = 0
                p.font.size = Pt(20)

        # 加入圖片
        if "image" in slide_data and image_dir:
            image_path = os.path.join(image_dir, slide_data["image"])
            # print(image_path)
            if os.path.exists(image_path):
                slide.shapes.add_picture(image_path, Inches(1), Inches(4.5), width=Inches(5.5))
                
        # 加入備忘稿文字
        if "description" in slide_data:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = slide_data["description"]
    
    prs.save(output_path)
    print(f"PowerPoint 檔案儲存為：{output_path}")
    
    # 不是付費會員，加浮水印
    if not prime:
        watermark(output_path, output_watermark_path)


def watermark(ppt_file, output_path,watermark_path='watermark/watermark.png', transparent_img='watermark/img_watermark'):
    # 製作半透明圖片
    def create_transparent_image(input_path, output_path, alpha=70):
        img = Image.open(input_path).convert("RGBA")
        # 修改 alpha（0 ~ 255）→ 100 表示大約 40% 不透明
        new_data = []
        for item in img.getdata():
            new_data.append((item[0], item[1], item[2], alpha))
        img.putdata(new_data)
        img.save(output_path, "PNG")

    # 路徑
    create_transparent_image(watermark_path, transparent_img)

    # 開啟簡報，加入浮水印
    prs = Presentation(ppt_file)
    
    # 浮水印尺寸（根據需求可調整）
    img_width = Inches(1.5)
    img_height = Inches(1.5)

    for slide in prs.slides:
        watermark_num = random.randint(2,3)

        for _ in range(watermark_num):
            x = Inches(random.uniform(0, 8.5))  # 預留空間避免超出邊界
            y = Inches(random.uniform(0, 6.0))

            slide.shapes.add_picture(transparent_img, x, y, width=img_width, height=img_height)

    # 儲存結果
    prs.save(output_path)

if __name__ == "__main__":
    json_data = 'Gemini/generate_output.txt'
    output_path = 'output_pptx/test.pptx'
    output_watermark_path = 'output_pptx/test_watermark.pptx'
    img_dir = 'Crop_imgs_demo'
    json_to_pptx(json_data, output_path, output_watermark_path, img_dir)
    