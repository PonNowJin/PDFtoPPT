# PDFtoPPT

```bash
pip install PyMuPDF opencv-python pytesseract
pip install layoutparser[layoutmodels,tesseract]

```

[PDF檔案]
   |
   v
[PDF解析器層] => PyMuPDF 開啟PDF、抽取圖片與文字區塊
   |
   v
[圖片過濾層] => 篩選：尺寸足夠、非背景圖、版面中段
   |
   v
[圖說對應層] => 擷取圖片附近區塊的圖說內容（Fig.1）
   |
   v
[儲存與輸出層] => 存成圖片 + metadata.json
